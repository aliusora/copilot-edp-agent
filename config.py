"""Configuration and constants for the application."""

SYSTEM_PROMPT = """You are a precise assistant for leadership Q&A about Microsoft Copilot (with Data Protection) for UNC-Chapel Hill.

IMPORTANT CONTEXT:
- UNC-Chapel Hill is part of the University of North Carolina system and uses Microsoft 365 Copilot as an enterprise tool.
- When answering UNC-specific questions, integrate information from both Microsoft documentation AND UNC/NIH-specific sources.
- UNC has its own policies, guidelines, and implementation practices that supplement Microsoft's documentation.

You MUST answer strictly from the SOURCES provided below. If sources are insufficient, reply:
"I can't answer due to a lack of approved sources."

Use clear bullets and include citations (title + URL) for any claims.
Be accessible to non-technical audiences while maintaining accuracy.

When citing sources, use the format: [Source Title](URL)

For UNC-specific questions, prioritize combining:
1. Microsoft's technical documentation on Copilot features and data protection
2. UNC's institutional policies and guidelines
3. NIH guidance when relevant to research contexts
"""

# UNC-specific and NIH-related authoritative sources
UNC_ENTERPRISE_SOURCES = [
    {
        'title': 'UNC ITS - Microsoft 365 Copilot for UNC',
        'url': 'https://its.unc.edu/ai/copilot/',
        'context': 'unc copilot enterprise deployment university',
        'summary': '''Microsoft 365 Copilot Chat (with Data Protection)
        Microsoft CopilotMicrosoft 365 Copilot Chat (with Data Protection) is an institutionally-scoped AI-powered assistant and generative AI tool, previously called Bing Chat Enterprise.

        Microsoft 365 Copilot Chat offers a higher level of data protection for organizations like UNC.

        Accessing Copilot Chat
        Microsoft 365 Copilot Chat (with Data Protection) is now available to anyone with an Onyen.

        Tar Heels can access Copilot directly or as part of the Microsoft Bing search engine. Be sure to sign into Copilot Chat with your UNC account before you begin to access the enterprise version with additional data protection.

        Ensure you are signing into your UNC account by using onyen@ad.unc.edu as your email address, as when logging into Heelmail or other online Microsoft 365 products.

        Copilot Chat does not support “strict” SafeSearch settings. Change your settings to “moderate” or “off” before accessing.

        Copilot Chat supports Microsoft Edge and other major non-Microsoft browsers like Chrome, Firefox and Safari. You can also download the mobile app from the App Store or Google Play.

        Why use Copilot
        Copilot Chat with Data Protection is a more secure alternative to consumer-oriented generative AI services like ChatGPT, Google Gemini or the non-enterprise version of Copilot (formerly known as Bing Chat).

        Employees can use Copilot Chat to quickly generate content, analyze or compare data, summarize documents, learn new skills, write code and much more. Instructors can use Copilot Chat to personalize learning, plan a lesson, brainstorm, tutor, communicate, analyze and improve efficiency.

        Copilot Chat also offers distinct advantages over other generative AI chat services, including built-in text-to-image generation and reference links and footnotes to make it easier to verify information.

        More secure
        Safeguarding information is the key benefit to using Copilot Chat (with Data Protection). When you use the enterprise version of Copilot Chat, Microsoft does not store or view your chats. Your queries are encrypted, and Microsoft does not use UNC-Chapel Hill data or queries to train any of its models.

        Your identity is used only to determine if you are eligible to access the tool. After you authenticate and access Copilot Chat (with Data Protection), your user identity information is removed. The basic version of Copilot Chat does not have access to your Microsoft 365 files.

        By comparison, tools like ChatGPT and Google Gemini store your searches and use your queries and chat history to train future models.

        Basic data protection guidance
        AI tools do not change the rules about safeguarding data at our institution. Your obligations under grants, contracts, data use agreements or other external obligations remain the same. Additionally:

        Do not use AI tools for protected health information (PHI), or data subject to HIPAA (Health Insurance Portability and Accountability Act), or Tier 3 data.
        While Copilot with Data Protection has the appropriate safeguards for Tier 1 and Tier 2 data, do check to make sure any external obligation, data management plans, or system security plans allow for the use of this tool. Those obligations would override any “safe for Tier 1 or Tier 2” designation.
        When in doubt whether something is appropriate, ask ITS for guidance. Err on the side of caution until you are certain.

        Learn more and use responsibly
        Microsoft has an abundance of materials from which you can learn much more about the tool, including

        Overview
        Tips and tricks
        Privacy and protections
        Discussion page

        Follow University guidelines about using AI tools appropriately and ethically. Early in 2023, the Provost tasked an AI committee and subcommittees with creating resources for University staff. Please refer to guidance for employees or guidance for students for campus-specific best practices.

        You must also safeguard the University’s and your own information. As you do with all information and tools, comply with federal and state privacy regulations and safe computing best practices. You have a responsibility to exercise due care over any data you submit to a third party.

        Technical support
        For technical support, contact the ITS Service Desk by visiting the Help Portal or calling 919-962-HELP (4357).
        '''
    },
    {
        'title': 'UNC AI Initiative - Research & Generative AI Usage Guidance',
        'url': 'https://ai.unc.edu/research-generative-ai-usage-guidance/',
        'context': 'unc policy generative ai guidelines university',
        'summary': '''Research Generative AI Usage Guidance
        To the UNC research community:

        As you are likely aware, the use of generative AI tools such as ChatGPT has sparked numerous inquiries related to research and scholarly practices. To address these and other emerging concerns, the Provost and Deans established the UNC Generative AI Committee, with representatives from every academic unit.

        The Committee has developed the following guidance for research and scholarly applications of generative AI. This guidance applies to all members of the research community, including faculty, staff (SHRA and EHRA non-faculty), students (undergraduate, graduate and professional), guest researchers (e.g., unpaid volunteers, interns, and visiting scholars), collaborators, and consultants involved in research occurring under the auspices of the University. This guidance aims to establish a framework for the ethical and responsible employment of AI tools in research and scholarship.

        Please review this guidance and integrate it into your research and scholarly practices, tailoring it as necessary to suit your specific discipline and accepted research and scholarly practices within your discipline. Mentors and supervisors should have regular conversations with mentees and other research trainees about the intended use of generative AI in their research programs.

        Given the rapid pace of advancements in generative AI, we anticipate this guidance to continue to evolve. Thus, if you have any questions or feedback, please do not hesitate to reach out to Eric Everett (Phone: 919-962-0988 or email: eric_everett@unc.edu).

        Research Use Guidance for Generative Artificial Intelligence
        Introduction
        Generative AI (Artificial Intelligence) systems such as ChatGPT have emerged from a number of technologies including machine learning and are capable of creating images, text, and other products in response to queries and prompts. As a result, generative AI has become a powerful tool for research and scholarship. Systems like ChatGPT can be task-specific and are capable of evolving as information is provided from users and other sources.

        Use of generative AI in research involves (at least) the following limitations and risks.
        The operations that produce AI output are often unknown to its end-users. As a result, these tools may generate content that is not amenable to verification via validating primary sources.
        AI-generated output is based on previously existing data and thus reflects the biases and other limitations of that data. These biases need be interrogated and acknowledged. The output may also be inaccurate or entirely fabricated, even if it appears reliable or factual.
        It cannot be assumed that generative AI tools are compliant with rules and laws designed to ensure the confidentiality of private information, such as HIPAA (Health Insurance Portability and Accountability Act of 1996) and FERPA (Family Educational Rights and Privacy Act). Uploading information (e.g., research data, grant proposals, unpublished manuscripts, or analytical results) to a public AI tool is equivalent to releasing it publicly; thus, before any information from you or another individual is uploaded to a public AI tool, appropriate steps must be taken to ensure that the disclosure of that information is consistent with all rules and laws related to the handling of private information.
        Generative AI may present other privacy risks to both individuals and the institution, such as those implicated by data breaches, exposure of intellectual property (IP), and Science & Security concerns.
        Generative AI raises a range of intellectual property concerns regarding the ownership of its output, as well as questions about whether its output is properly treated as equivalent to a published resource. In particular, generative AI may create content that infringes on others’ intellectual property (IP) or copyright-protected works. Generative AI may also create content that leads to allegations of plagiarism or other forms of misconduct against the researcher or scholar.
        Norms and requirements surrounding the citation of AI-generated output, as well as disclosure of the use of AI technologies, are complex, rapidly evolving, and oftentimes unclear. In addition, these norms and requirements may vary substantially depending on the source; for example, publishers, journals, professional organizations, and funding organizations all may have (or be in the process of developing) policies surrounding the use of AI that need to be navigated.

        Usage Philosophy
        University of North Carolina at Chapel Hill policy is that its research be carried out with the highest standards of integrity and ethical behavior. To that end, everyone involved in conducting research under the auspices of the University is responsible for ensuring that they use best practices in proposing, performing, and reviewing research, as well as in reporting research results. Authors are ultimately responsible and accountable for the content and methodology of their published and disseminated work.

        Lead Principal Investigators and other key personnel involved in the preparation of grant applications submitted through the University’s Research Administration Management System & eSubmission (RAMSeS) certify the submissions before the grants are sent to sponsors. This entails certifying the following:

        The information submitted within this application is true, complete, and accurate to the best of my knowledge. Any false, fictitious, or fraudulent statements or claims may subject the Organization and the Investigators to criminal, civil, or administrative penalties.
        I have the responsibility for the scientific, fiscal, and ethical conduct of the project and to provide the required progress reports if an award is made.
        I will comply with all relevant state and federal regulations, University policies, and contractual obligations in administering the resultant award.
        I have reviewed applicable U.S. Export Control requirements and University policy on Export Controls and will comply with the export control requirements.
        If this is an NIH application, I will comply with NIH Policy on Public Access.
        I will work to ensure that my relationship with the sponsor of this project is free of conflict of interest or consistent with a previously disclosed conflict of interest management plan.
        I can ensure that proper citation practices have been followed in this submission; and
        The information that is proposed in this application represents original work by the investigators named in the application.

        Usage of generative AI in research should be based on the following principles:
        Entering private or confidential information into a public AI tool is tantamount to publicly releasing that information. Uploading information to public AI tools, including by entering prompts or queries into tools like ChatGPT, is a form of release of that information to a third party. The same rules that apply to other forms of public disclosure of private or confidential information apply as well to interactions with public generative AI tools. Disclosure of this type of information to public AI tools exposes both individuals and the institution to potential breaches of privacy and security. Similarly, uploading research data, grant proposals, or analytical results into a public AI tool is effectively to disclose that content publicly.
        The norms of appropriate use of generative AI are constantly evolving, and vary enormously depending on application, context, and discipline. A particular use of generative AI in one research context might be perfectly appropriate, whereas an identical use of generative AI in a different research context might be a serious breach of professional research standards.
        Those who are involved in proposing, reviewing, performing, or disseminating research bear the responsibility for familiarizing themselves with the policies and standards governing the use of generative AI in their research, and are ultimately responsible for the work that they produce and disseminate. This responsibility includes properly attributing ideas and credit, ensuring the accuracy of facts, relying on authentic sources, and appropriately disclosing the use of AI in research. This responsibility applies to all members of the research community, including faculty, students, staff, postdoctoral research scholars, and other research trainees. Individuals with supervisory responsibility for research activities should initiate discussions with their teams to ensure that all members of the team understand both opportunities and responsibilities surrounding the use of generative AI.
        The use of generative AI should be clearly and transparently disclosed and documented. Documentation requirements will vary substantially from research context to research context and from discipline to discipline, but researchers should err on the side of explicitly disclosing any material use of generative AI in their research activities. Here is one perspective, generated by the Association for Computing Machinery:

        “If you are using generative AI software tools such as ChatGPT, Jasper, AI-Writer, Lex, or other similar tools to generate new content such as text, images, tables, code, etc. you must disclose their use in either the acknowledgements section of the Work or elsewhere in the Work prominently. The level of disclosure should be commensurate with the proportion of new text or content generated by these tools.
        If entire sections of a Work, including tables, graphs, images, and other content were generated by one of these tools, you should disclose which sections and which tools and tool versions you used to generate those sections by preparing an Appendix or a Supplementary Material document that describes the use, including but not limited to the specific tools and versions, the text of the prompts provided as input, and any post-generation editing (such as rephrasing the generated text). Authors should also note that the amount or type of generated text allowable may vary depending on the type of the section or paper affected. For example, using such tools to generate portions of a Related Work section is fundamentally different than generating novel results or interpretations.
        If the amount of text being generated is small (limited to phrases or sentences), then it would be sufficient to add a footnote to the relevant section of the submission utilizing the system(s) and include a general disclaimer in the Acknowledgements section.
        If you are using generative AI software tools to edit and improve the quality of your existing text in much the same way you would use a typing assistant like Grammarly to improve spelling, grammar, punctuation, clarity, engagement or to use a basic word processing system to correct spelling or grammar, it is not necessary to disclose such usage of these tools in your Work.”

        Researchers should also be aware of or anticipate other positions coming from journals, publishers, professional associations and societies, and funders or sponsors regarding the use of generative AI in the creation of new content.
        It is a shared responsibility to stay informed about relevant developments surrounding generative AI. Both the technical capabilities of generative AI tools and the rules and norms surrounding their use are constantly evolving, and responsible research requires an up-to-date awareness of changes in AI technology and best practices within specific fields of research and scholarship. Everyone involved in research should make efforts to stay informed about relevant emerging AI tools, research studies, and ethical guidelines, and should take advantage of professional development opportunities to enhance their AI integration skills.
        '''
    },
    {
        'title': 'UNC Graduate Handbook - Generative AI Policy',
        'url': 'https://handbook.unc.edu/generativeai.html',
        'context': 'unc research ai guidance best practices university',
        'summary': '''Guidance on Generative AI Use
        Following the guidance from UNC's Generative AI Committee, The Graduate School's Administrative Board encourages graduate programs to embrace the philosophy guiding the recommended language “that humans are responsible for the use of generative AI and that 'AI should help you think. Not think for you.'”

        The Board maintains that generative artificial intelligence (AI) can be a productive tool and foster new directions and perspectives for the teaching and research environment in institutions of higher education. Users of generative AI, following University guidelines, should take full responsibility for their use of AI and any research that might result from the use of generative AI tools.

        Specific to graduate education, the Board recognizes that embracing generative AI tools may have nuanced applications for graduate students, faculty advisors, and degree program administrators.

        Student Generative AI Usage Guidance
        Individual graduate programs may establish guidelines specific to their thesis and comprehensive exams depending on their specific format.
        If generative AI use is encouraged in a program, guidance developed for the campus related to student use should also apply to graduate students in their own classes and research.
        Students should remember that they are always subject to the UNC Honor Code.

        Teaching Generative AI Usage Guidance
        Guidance developed for the campus related to teaching use should also apply to instructors, including teaching assistants.
        Programs can encourage TAs to connect with supervising faculty to ensure any enrolled student usage complies with class guidelines and the supervisor supports the TA using AI in their own grading or teaching work.
        Graduate programs should share these resources and guidance with any graduate students serving as TAs.

        Research Generative AI Usage Guidance
        Graduate student research is collaborative. Any use of AI for research and writing purposes should be discussed with supervisors, advisors, committee members, and any other associated individuals.
        Be aware that use of AI might lead to data leakage and proliferation, permanence, and widespread availability for unverified data.

        Suggestions for topics of discussion between students and advisors regarding use of AI:
        - Order of writing and editing and using these tools, and how to incorporate its use and permissions for publishing purposes.
        - Discussion of appropriate journal policies and granting agency policies relevant to the field of study regarding AI use and publication practices.
        - Discuss considerations and challenges for intellectual property (i.e., certain journals may disallow submission of material that has been previously submitted to AI sites as it may fall under the category of previously published in a public space).
        - Discuss methods or development of research design, drafts and writing generation and editing, analysis of data generated through AI, use of AI to develop any media associated with the work, or any presentation materials, including but not exhaustive to the following:
        - Citations and/or a statement disclosing specific uses of AI
        - Include appendix documenting any exchanges (input or output of materials, texts, or data) using AI
        - Including a methods section of final research/products explaining the use of AI and its impact on research/products
        '''
    },
    {
        'title': 'UNC School of Medicine - Safe Uses and Best Practices of AI Tools',
        'url': 'https://www.med.unc.edu/spo/2025/04/safe-uses-and-best-practices-of-ai-tools-at-unc/',
        'context': 'unc medical school ai safety best practices healthcare',
        'summary': '''Safe Uses and Best Practices of AI Tools at UNC
        The letter was sent out by the Office of the CIO on April 9, 2025.

        This email, provided by the Office of the CIO, addresses questions surrounding artificial intelligence (AI) tools and programs, emphasizing the exclusive use of Microsoft Bing Copilot for institutional activities. It outlines guidelines, precautions, and ethical considerations to ensure secure and responsible use of AI. Topics include data protection protocols, limitations on sensitive data usage, and best practices for integrating AI into work while safeguarding accuracy, integrity, and ethical standards. Resources and training opportunities are provided for a seamless and informed AI experience.

        Dear Students, Faculty, and Staff,
        Many of you continue to raise questions about opportunities and concerns with artificial intelligence tools and programs. This email endeavors to provide practical advice on the use of AI, emphasizing the exclusive use of Microsoft Bing Chat and Copilot, and outlining necessary precautions and considerations for employing other AI tools.

        Exclusive Use of Microsoft Bing Copilot
        Microsoft Bing Copilot is the only Generative AI tool approved for general use. All other AI tools must go through security and data governance review to safeguard institutional data. Do not use personal AI accounts (even personal Microsoft accounts) with university data.

        Security and Data Concerns
        Other GenAI tools lack the same level of security and data protection as Microsoft Copilot due to guardrails in place within our relationship with Microsoft. Our institution is obligated to adhere to strict data privacy regulations and security protocols, particularly when handling sensitive data. Unauthorized use of non-approved AI tools could compromise the confidentiality and integrity of our data.

        AI tools do not change the rules about data. Your obligations under grants, contracts, data use agreements, or other external obligations remain the same. Additionally:
        - Do not use AI tools for data subject to HIPAA (Health Insurance Portability and Accountability Act) or Tier 3 data, which includes social security numbers, credit card information, and other restricted data (more information on data classification can be found on the UNC Information Classification page).
        - While Bing Chat Enterprise has the appropriate safeguards for Tier 1 and Tier 2 data, make sure any external obligation, data management plans, or system security plans allow for the use of this tool. Those obligations override any “safe for Tier 1 or Tier 2” designation.

        Ethical Considerations:
        - Do Not Let AI Think FOR You: AI tools, including Microsoft Copilot, are designed to assist and augment human capabilities, not replace them. Always use AI as a supportive tool rather than relying on it to make decisions or generate content autonomously. Apply your professional judgment and expertise when interpreting AI-generated outputs.
        - Check Citations and Accuracy: When using AI to assist with research or educational content creation, verify the accuracy of the information provided. Cross-check citations and ensure that the data is reliable and up to date to maintain credibility and integrity.
        - Bias Awareness: AI tools can reflect biases present in the data they were trained on. Be vigilant about recognizing and mitigating potential biases in AI-generated content.

        Using Microsoft Bing Copilot While Logged into Your M365 Account
        To ensure a secure and efficient experience with Microsoft Copilot, follow these steps to correctly log into your M365 account:
        1. Open Microsoft Edge.
        2. Go to copilot.microsoft.com.
        3. Navigate to the “Sign In” option, usually located in the top-right corner of the application window.
        4. Enter your work email address (ONYEN@ad.unc.edu) and click “Next.”
        5. Provide your password and complete any additional authentication steps (e.g., two-factor authentication).
        6. Once logged in, access Microsoft Copilot through the designated toolbar or menu within the application.
        Warning: If you are not signed in, you are using the public Bing Copilot.

        Best Practices:
        - Be Specific: When using Bing Chat, be specific in your prompts to get the most accurate and relevant responses.
        - Provide Context and Instructions: Give Copilot background information and guidance on what you want it to do. For example: “Write a summary of this article in three sentences, highlighting the main point for an audience of biomedical engineering graduate students.”
        - Use Examples and Provide Feedback: Show Copilot examples of the desired output or format, and provide feedback on responses to improve accuracy.

        Copilot Training and Resources
        - UNC Provost’s Gen AI Usage Guidelines for Research Community
        - UNC Provost’s Gen AI Resources for Administration and Staff
        - UNC Provost’s Gen AI Usage Guidelines for Faculty
        - UNC University Libraries Student Guide to Generative AI

        Consider these resources from LinkedIn Learning and Carolina AI Literacy (available for free to all UNC faculty, staff, and students):
        - Get Started with Microsoft Copilot
        - Prompt Engineering: How to Talk to the AIs
        - Carolina AI Literacy (unc.edu) hosts videos and modules to train University members on how to interact with tools like BCE, including writing appropriate prompts. This material focuses on the educational mission but is useful for learning how to interact with Generative AI tools, including understanding biases and fact checking.

        The integration of AI tools like Microsoft Copilot presents exciting opportunities. By adhering to the guidelines and best practices outlined in this document, faculty and staff can harness the power of AI while maintaining the highest standards of security, accuracy, and ethical responsibility.

        Should you have any questions or require further assistance, please contact the IT support team.
        '''
    },
    {
        'title': 'Information Classification Standard',
        'url': 'https://policies.unc.edu/TDClient/2833/Portal/KB/ArticleDet?ID=131244',
        'context': 'unc policy teaching research academic ai university',
        'summary': '''University of North Carolina at Chapel Hill Information Classification Standard
        Introduction
        Purpose
        The Information Classification Standard sets a framework for the University of North Carolina's ("University" or "UNC-Chapel Hill") information. This framework helps us recognize, manage, and protect the types of University information we handle. The classification aligns with the Information Security Controls Standard (“MSS”) which sets the security measures needed. In some cases, data obligations include responsible data sharing driven by the University’s mission, scholarship, and research. Proper data management also involves data integrity, accuracy, and availability (e.g., records management). Classification is the first step to understanding how to properly handle University Information.

        The University classifies information according to:
        - Law, regulation, administrative, and contractual requirements;
        - Ethical considerations;
        - Strategic or proprietary value; and
        - Operational use.

        Classifying information correctly gives everyone at the University a framework that supports their University activities.

        Scope
        This policy applies to all members of the UNC-Chapel Hill community including faculty, employees, students, and contractors.

        Standard
        This standard defines four tiers of information:
        - Tier 0: Public Information
        - Tier 1: Business Information
        - Tier 2: Confidential Information
        - Tier 3: Restricted Information

        Classifying information is an ongoing process. Information may shift between tiers many times throughout its existence, or fall into different tiers based on its context. Seek guidance when a classification is not clear.

        The University has three missions: education, research, and public service. Classification supports all three as some types of information must be more readily available than others.

        Examples and descriptions of information elements are below.

        GENERAL INFORMATION

        Tier 0: Public Information
        Public Information, or Tier 0, is information that is approved to be published. There are no limits on disclosing public information. Information the University has published or intends to publish is Tier 0. Protecting Tier 0 information means protecting its accuracy, source authority, and integrity. Tier 0 information directs to MSS “Low” baseline controls by default.

        Examples of Public Information:
        - Information in the University directory the public can see.
        - Information on University websites the public can see, such as:
        - Marketing material
        - Descriptions of departments or programs
        - Press releases
        - Requests to take part in research
        - Business information that is archived (with limited exceptions).
        - Annual Clery reports.

        Tier 1: Business Information
        The public does not have direct access to Business Information, called Tier 1. Mainly for internal use, Business Information is usually about operating the University.

        To protect Tier 1 information, controls are in place on who can access it. By default, those controls are reflected in the MSS “Low” baseline controls. Everyone who uses Tier 1 information must protect it.

        As part of doing work, a person may need to share Tier 1 information with others who need it to do their work. Tier 1 information can be shared with others at the University who have a business need for it.

        Those with access to Tier 1 information should only share it with someone outside the University if their job requires it and only the information needed.

        Examples of Business Information:
        - Memos, correspondence, meeting minutes, contact lists, or procedures (not otherwise restricted).
        - Records of budgets or purchases, including reports and vendor catalogs or brochures.
        - Chemical safety records such as Employee Right-To-Know reports.
        - Grant proposals and supporting documents once the grant is complete.
        - Information in the “twelve categories” that North General Statute § 126-23 identifies for personnel records.
        - Student information defined as “FERPA directory information” but not published. (Published information is Tier 0.)
        - PID, Onyen
        - Unpublished findings from research (unless rated at a higher Tier because of their content, such as SSNs, clinical data protected by HIPAA, or data under nondisclosure or other confidentiality agreements)
        - Intellectual property unless rated at a higher Tier due to their content or under nondisclosure or other confidentiality agreements.

        SENSITIVE INFORMATION
        Tier 2 and Tier 3 information is "sensitive information" as it relates to University policies, standards, and procedures.

        University units handling sensitive information must review how they classify and manage it. NOTE: All Sensitive information directs by default to baseline MSS "Moderate" (Tier 2) or "High" (Tier 3). See the MSS for additional "overlay" controls that may also apply. Items that the University Records Retention Schedule marks "Confidential" often contain elements that are Tier 2 Confidential or Tier 3 Restricted.

        Tier 2: Confidential Information
        Tier 2 is typically information the University is required to keep confidential due to an external obligation. Examples include:
        - Law
        - Regulation
        - Contract
        - State or System Office policy

        Tier 2 is the default classification until a different classification is identified. Confidential Information includes information the University must keep confidential. For example:
        - Education records such as grades and class schedules protected by the Family Educational Rights and Privacy Act (FERPA)
        - The University's proprietary information including:
        - Findings from research
        - Intellectual property
        - Donor/funding sources that this standard does not put in a different Tier
        - Information in personnel files that the N.C. Human Resources Act protects. This includes the results of criminal background checks.
        - Communications between attorneys and clients.
        - Information subject to a confidentiality agreement.
        - Information protected by contract or non-disclosure agreement, e.g., vendor product roadmaps or sealed bids.

        Tier 2 information directs to MSS "Moderate" baseline controls by default. Also check for an Overlay that may apply.

        Tier 3: Restricted Information
        Restricted Information, or Tier 3, is information that is often called “need to know.” It should be shared with specific individuals only. Tier 3 has safety requirements set by external obligations the University must fulfill derived primarily from law, but potentially other sources as well.

        The University must use rigorous protections for Restricted Information. MSS "High" baseline controls apply by default, and most Tier 3 information will have additional Overlay controls as well. Loss or unauthorized disclosure may require notification or fines. In some cases, improper disclosure may lead to criminal penalties. Tier 3 data is primarily personal information that could harm people if disclosed improperly.

        Examples of Restricted Information:
        - Some education records protected by FERPA such as:
        - Disciplinary conduct reports
        - Student health information
        - Sexual assault reports
        - Passports
        - Financial aid information
        - Identifiable data subject to the “Common Rule.”
        - Protected Health Information as defined by HIPAA.
        - Financial Information covered by the North Carolina Identity Theft Protection Act of 2005.
        - Information controlled under ITAR and EAR export regulations.
        - Information covered by the Gramm-Leach-Bliley Act (GLBA).
        - Passwords and other authentication credentials unique to a person.
        - Social security numbers.

        Exceptions
        If a classification is not clear, seek guidance from the University’s Data Governance authorities. The site datagov.unc.edu provides guidance and a link to request “Data Assistance.” The Data Governance Oversight Group can provide authoritative information on classification, new determinations, and any exceptions to this Standard. Exceptions may:
        - Clarify context
        - Address legal requirements
        - Address a work need
        - Protect the welfare of people
        - Address risk level
        - Resolve conflicts in classification

        Definitions
        Information: Any communication or representation of knowledge such as facts, data, or opinions in any medium or form, including textual, numerical, graphic, cartographic, verbal, or audio/visual.
        Risk of harm: Risk to the University's mission, compliance, finances, operations, and/or reputation.
        University Data: Also called University Information or Enterprise Data. Includes any data the University has a legal, business, or ethical responsibility or right to protect or share.

        Related Requirements
        External Regulations and Consequences:
        - U.S. Department of Health and Human Services – Federal Policy for the Protection of Human Subjects ("Common Rule")
        - U.S. Department of Health and Human Services – Health Information Privacy
        - U.S. Public Law 106-102: Gramm-Leach-Bliley Act (GLBA)
        - U.S. International Trade Administration – U.S. Export Regulations
        - Family Educational Rights and Privacy Act (FERPA)
        - North Carolina General Statutes, Chapter 75, Article 2A – N.C. Identity Theft Protection Act
        - North General Statute § 126-23 – Certain Records to be Kept by State Agencies Open to Inspection
        - North Carolina General Statutes, Chapter 126 – N.C. Human Resources Act
        - PCI Security Standards Council – Payment Card Industry Data Security Standards (PCI DSS)

        Failure to comply with this standard may put University information assets at risk and have disciplinary consequences for employees, up to and including termination. Students who fail to adhere to this standard may be referred to the UNC-Chapel Hill Office of Student Conduct. Contractors, vendors, and others who fail to comply may face termination of their business relationships with UNC-Chapel Hill.

        Violation of this standard may also carry civil or criminal penalties.

        University Policies, Standards, and Procedures:
        - Records Management Policy
        - General Records Retention and Disposition Schedule
        - Export Controls Policy

        Contact Information
        Primary Contacts:
        Subject: Standard Questions
        Contact: ITS Policy Office
        Telephone: 919-962-HELP
        Online/Email: help.unc.edu

        Subject: Classification and related guidance
        Contact: UNC-Chapel Hill ITS Information Security Office
        Telephone: 919-962-HELP
        Online/Email: help.unc.edu ("University Data Assistance Request")

        Subject: Report a Violation
        Contact: UNC-Chapel Hill ITS Information Security Office
        Telephone: 919-962-HELP
        '''
    },
    {
        'title': 'NIH - AI Use in Research Applications Policy',
        'url': 'https://grants.nih.gov/news-events/nih-extramural-nexus-news/2025/07/apply-responsibly-policy-on-ai-use-in-nih-research-applications-and-limiting-submissions-per-pi',
        'context': 'nih grants research ai policy applications federal',
        'summary': '''Apply Responsibly: Policy on AI Use in NIH Research Applications and Limiting Submissions per PI
        NIH has recently announced a new policy that will continue to support originality, creativity, and fairness in the research application process. NIH has noticed that some Principal Investigators (PIs) have been submitting a large number of research applications that far exceed the numbers we traditionally expect and may have been prepared using artificial intelligence (AI) tools.

        While AI may be a helpful tool in preparing applications, the rapid submission of large numbers of research applications from a single PI may undermine the fairness and originality of the research application process and unfairly strain NIH’s application review processes.

        As use of AI tools becomes more commonplace, it is important to remember that applicants may use AI in limited aspects to reduce administrative burden while preparing applications. However, applicants should be mindful of the concerns around research misconduct or lack of originality when using such tools. Remember, NIH peer reviewers are prohibited from using AI for their critiques.

        To address these issues, the new policy is effective for the September 25, 2025, receipt date and beyond:

        - Applications that are either substantially developed by AI or containing sections substantially developed by AI are not considered the original ideas of applicants and will not be considered by NIH.
        - NIH will also only accept up to six new, renewal, resubmission, or revision applications from an individual PD/PI (Program Director/Principal Investigator) or Multiple Principal Investigator for all council rounds in a calendar year. For more details on applicability, investigator roles, and impacted application types, please see these new FAQs.

        Based on historical data, we expect this policy will impact a relatively small number of investigators. For example, in 2024 only 1.3% of applicants submitted more than six applications.

        We appreciate the research community’s continued interest in ensuring applications submitted to NIH remain representative of their original thought and creativity. This policy will allow NIH to continue to advance biomedical research and appropriately steward taxpayer dollars.
        '''
    },
    {
        'title': 'NIH Notice - Use of Generative AI Technologies in NIH Grant Applications',
        'url': 'https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html',
        'context': 'nih notice ai grant applications policy federal',
        'summary': '''Supporting Fairness and Originality in NIH Research Applications
        Notice Number: NOT-OD-25-132

        Key Dates
        Release Date: July 17, 2025

        Related Announcements
        July 23, 2018 – NIH/AHRQ Application Submission/Resubmission Policy. See Notice NOT-OD-18-197.

        Issued by
        NATIONAL INSTITUTES OF HEALTH (NIH)

        Purpose
        NIH is providing guidance to researchers on the appropriate usage of artificial intelligence (AI) to maintain the fairness and originality of NIH’s research application process. NIH is also instituting a new policy limiting the number of applications that NIH will consider per Principal Investigator per calendar year.

        Background
        NIH has recently observed instances of Principal Investigators submitting large numbers of applications, some of which may have been generated with AI tools. While AI may be a helpful tool in reducing the burden of preparing applications, the rapid submission of large numbers of research applications from a single Principal Investigator may unfairly strain NIH’s application review processes.

        The percentage of applications from Principal Investigators submitting an average of more than six applications per year is relatively low; however, there is evidence that the use of AI tools has enabled Principal Investigators to submit more than 40 distinct applications in a single application submission round.

        NIH will continue to employ the latest technology in detection of AI-generated content to identify AI-generated applications, but it is imperative that all NIH research applications are consistent with the NIH Grants Policy Statement (GPS) Section 2.1.2’s expectation that institutions and affiliated research teams propose original ideas for funding.

        AI tools may be appropriate to assist in application preparation for limited aspects or in specific circumstances, but researchers should be aware that using AI comes with its own risks. AI use may result in plagiarism, fabricated citations, or other kinds of research misconduct. As a reminder, NIH oversees research misconduct investigations and acts on non-compliance (see GPS Section 4.1.27).

        Policy
        NIH will not consider applications that are either substantially developed by AI or contain sections substantially developed by AI to be original ideas of applicants. If the detection of AI is identified post award, NIH may refer the matter to the Office of Research Integrity to determine whether there is research misconduct while simultaneously taking enforcement actions including, but not limited to:
        - Disallowing costs
        - Withholding future awards
        - Wholly or in part suspending the grant
        - Possible termination

        NIH will only accept six new, renewal, resubmission, or revision applications from an individual Principal Investigator/Program Director or Multiple Principal Investigator for all council rounds in a calendar year. This policy applies to all activity codes except T activity codes and R13 Conference Grant Applications.

        Based on recent data, this limit will affect a relatively small number of Principal Investigators while enabling the NIH to maintain consistently high-quality grant application review and appropriately steward taxpayer dollars.

        Effective Date
        This policy is effective for applications submitted to the September 25, 2025, receipt date and beyond.
        '''
    }
]

# Default settings
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 1500
DEFAULT_NUM_SOURCES = 5
DEFAULT_CACHE_TTL_HOURS = 24