# agent/llm_mixtral_local.py
"""
Local Mixtral-8x7B-Instruct wrapper for offline LLM inference.

Design goals:
- Tiny public API with one class (LocalMixtral) and one main method (complete).
- Explicit, typed configuration (LocalConfig dataclass).
- Offline by default; load weights from a local directory.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from .types import LLMResponse, Citation


# ----------------------------- #
# 1) Configuration (data class) #
# ----------------------------- #

@dataclass(frozen=True)
class LocalConfig:
    """
    Immutable configuration for the local LLM.

    Attributes:
        model_path: Filesystem path to the local Mixtral-8x7B-Instruct weights.
        load_in_4bit: Use 4-bit quantization to reduce VRAM.
        max_new_tokens: Cap on generated tokens for determinism/cost control.
        temperature: Sampling temperature (0.0 => more deterministic).
        device_map: 'auto' lets Accelerate place layers across devices if present.
    """
    model_path: Path
    load_in_4bit: bool = True
    max_new_tokens: int = 600
    temperature: float = 0.2
    device_map: str = "auto"


# ------------------------------------------ #
# 2) The model wrapper (class + two methods) #
# ------------------------------------------ #

class LocalMixtral:
    """
    A minimal, testable wrapper around a local Mixtral-8x7B-Instruct model.

    Public API:
      - __init__(cfg: LocalConfig)
      - complete(system: str, user: str, sources: Iterable[str]) -> LLMResponse
    """

    def __init__(self, cfg: LocalConfig) -> None:
        """Initialize tokenizer and model from local disk with optional 4-bit quantization."""
        self.cfg = cfg

        quant_cfg = None
        if cfg.load_in_4bit:
            quant_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_use_double_quant=True,
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        # Load tokenizer & model from local path (offline mode recommended via env vars)
        model_path_str = str(cfg.model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(model_path_str, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path_str,
            device_map=cfg.device_map,
            torch_dtype=(torch.bfloat16 if not cfg.load_in_4bit else None),
            quantization_config=quant_cfg,
            low_cpu_mem_usage=True,
        )

        # Safety: ensure pad_token_id exists (fall back to EOS if missing)
        if self.tokenizer.pad_token_id is None and self.tokenizer.eos_token_id is not None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

        self.model.eval()  # inference mode (no gradients)

    # ---- Internal helper (private by convention) ---- #
    def _build_prompt(self, system: str, user: str, sources_block: str) -> str:
        """
        Build an instruction-formatted prompt for Mixtral-8x7B-Instruct.

        The instruct variant expects [INST]...[/INST] sections. We include:
        - system guidance (rules),
        - curated SOURCES (from MCP),
        - the user question.
        """
        return (
            "<s> [INST] "
            + system.strip()
            + "\n\n[SOURCES]\n"
            + sources_block.strip()
            + "\n\n[USER]\n"
            + user.strip()
            + " [/INST]"
        )

    # ---- Public method called by the rest of your app ---- #
    def complete(self, system: str, user: str, sources: Iterable[str]) -> LLMResponse:
        """
        Generate a grounded answer. If SOURCES are missing/empty, the SYSTEM
        prompt should instruct the model to decline to answer.

        Transformations:
          str -> tokenize -> torch tensors on GPU -> generate -> decode -> str
        """
        # 1) Compose SOURCES (data organization)
        src_lines: List[str] = []
        for i, s in enumerate(sources, start=1):
            s_clean = s.strip()
            if s_clean:
                src_lines.append(f"[{i}] {s_clean}")
        sources_block = "\n".join(src_lines) if src_lines else "No approved sources."

        # 2) Prompt assembly (pure string transformation)
        prompt = self._build_prompt(system, user, sources_block)

        # 3) Tokenization (text -> ids -> tensors on device)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        # 4) Generation under inference-only context (faster, lower memory)
        with torch.inference_mode():
            out = self.model.generate(
                **inputs,
                max_new_tokens=self.cfg.max_new_tokens,
                temperature=self.cfg.temperature,
                do_sample=(self.cfg.temperature > 0.0),
                pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
            )

        # 5) Decode back to text
        text = self.tokenizer.decode(out[0], skip_special_tokens=True)

        # 6) Best-effort extraction of citations (simple text processing)
        citations: List[Citation] = []
        for line in text.splitlines():
            if line.strip().startswith("- ") and "http" in line:
                head, url_part = line.split("http", 1)
                title = head.lstrip("- ").strip(" —:-")
                url = "http" + url_part.strip("). ]")
                citations.append(Citation(title=title or "Source", url=url))

        return LLMResponse(text=text, citations=citations)