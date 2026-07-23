from django.core.management.base import BaseCommand
from portfolio.models import Profile, Skill, Project, Experience, Education, Certification, Blog, SocialLinks
import json

class Command(BaseCommand):
    help = 'Seeds the portfolio database with S Sreesh\'s resume and project details'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 1. Profile
        Profile.objects.all().delete()
        profile = Profile.objects.create(
            name="S Sreesh",
            title="Software Developer | Python Developer",
            location="Kerala, India",
            email="ssreesh45@gmail.com",
            phone="+91 81294 10562",
            linkedin="https://www.linkedin.com/in/s-sreesh",
            github="https://github.com/Sreesh-S",
            portfolio_url="https://sreesh-portfolio.vercel.app/",
            bio=(
                "Aspiring Python Developer completed Master of Computer Applications with a strong interest in "
                "Software Development. Experienced in developing academic and project-based applications involving "
                "data processing, backend development, and full-stack implementation. Built practical solutions that "
                "demonstrate the ability to translate theoretical concepts into functional software systems. Possess "
                "a solid understanding of software development principles, structured problem-solving, and efficient "
                "application design. Committed to continuous learning and eager to contribute to real-world software "
                "projects in a professional environment."
            ),
            languages="English, Malayalam, Hindi",
            soft_skills="Problem Solving, Analytical Thinking, Team Collaboration, Time Management, Continuous Learning"
        )
        self.stdout.write(f'Created profile for: {profile.name}')

        # 2. Skills
        Skill.objects.all().delete()
        skills_data = [
            # Programming
            ('Python', 'Programming', 95, 'fa-brands fa-python', '#00F5FF'),
            ('Java', 'Programming', 80, 'fa-brands fa-java', '#7B61FF'),
            ('C', 'Programming', 75, 'fa-solid fa-c', '#39FF14'),
            
            # Web
            ('HTML', 'Web', 92, 'fa-brands fa-html5', '#FF5733'),
            ('CSS', 'Web', 90, 'fa-brands fa-css3-alt', '#29B6F6'),
            ('JavaScript', 'Web', 85, 'fa-brands fa-js', '#FFD600'),
            ('Node.js', 'Web', 80, 'fa-brands fa-node-js', '#4CAF50'),
            ('PHP', 'Web', 75, 'fa-brands fa-php', '#00E5FF'),
            ('Django', 'Web', 92, 'fa-solid fa-cubes', '#00F5FF'),
            
            # Data
            ('Power BI', 'Data', 80, 'fa-solid fa-chart-line', '#FFD600'),
            ('Data Visualization', 'Data', 85, 'fa-solid fa-chart-pie', '#7B61FF'),
            ('Data Analysis', 'Data', 85, 'fa-solid fa-magnifying-glass-chart', '#00F5FF'),
            
            # Database
            ('MySQL', 'Database', 85, 'fa-solid fa-database', '#00E5FF'),
            ('MongoDB', 'Database', 80, 'fa-solid fa-server', '#4CAF50'),
            
            # Tools
            ('Git', 'Tools', 90, 'fa-brands fa-git-alt', '#FF5722'),
            ('GitHub', 'Tools', 95, 'fa-brands fa-github', '#FFFFFF'),
            ('Software Testing', 'Tools', 85, 'fa-solid fa-vial-circle-check', '#39FF14'),
        ]
        
        for name, cat, prof, icon, glow in skills_data:
            Skill.objects.create(name=name, category=cat, proficiency=prof, icon_class=icon, hover_glow=glow)
        self.stdout.write(f'Seeded {len(skills_data)} skills.')

        # 3. Projects
        Project.objects.all().delete()
        
        # Project 1: DDoS
        p1 = Project.objects.create(
            title="Machine Learning Based DoS/DDoS Attack Detection System",
            subtitle="Cyber Security Intrusion Detection System",
            description="Developed a Django-based Intrusion Detection System (IDS) to detect and classify DoS/DDoS attacks using Machine Learning. Trained a Random Forest classifier on the CICIDS2017 dataset for accurate network traffic classification.",
            long_description=(
                "### Project Overview\n"
                "• Developed a Django-based Intrusion Detection System (IDS) to detect and classify DoS/DDoS attacks using Machine Learning.\n"
                "• Trained a Random Forest classifier on the CICIDS2017 dataset for accurate network traffic classification.\n"
                "• Built real-time prediction, attack logging, and reporting modules with an interactive security dashboard.\n"
                "• Implemented data preprocessing and demonstration-level IP mitigation for detected malicious traffic.\n\n"
                "### Key Implementation Details\n"
                "The project utilizes Python socket programming and Scapy to capture network packet structures. "
                "Packet fields are mapped to a trained Random Forest model. Security parameters are displayed on an "
                "interactive browser dashboard built with Django."
            ),
            image="projects/ddos_main.jpg",
            tech_stack="Python, Django, Scikit-learn, Pandas, NumPy, SQLite, HTML, CSS, JavaScript",
            github_url="https://github.com/Sreesh-S/DoS-DDoS-Attack-Detection-System",
            live_url="",
            is_featured=True,
            features=json.dumps([
                "Developed a Django-based Intrusion Detection System (IDS) to detect and classify DoS/DDoS attacks using Machine Learning.",
                "Trained a Random Forest classifier on the CICIDS2017 dataset for accurate network traffic classification.",
                "Built real-time prediction, attack logging, and reporting modules with an interactive security dashboard.",
                "Implemented data preprocessing and demonstration-level IP mitigation for detected malicious traffic."
            ]),
            challenges=(
                "Aligning raw real-time socket flows to match the static features defined in the CICIDS2017 training dataset. "
                "We solved this by creating a pipeline that computes packet variances and inter-arrival times dynamically over sliding time windows."
            )
        )

        # Project 2: Blood Report
        p2 = Project.objects.create(
            title="Smart Blood Report Analyzer & Disease Predictor",
            subtitle="OCR-Powered Diagnostic Tool",
            description="Developed a Python-based machine learning application to analyze blood reports using OCR technology. Extracted medical parameters from PDF and image-based reports. Built predictive models to identify diseases such as anemia and leukemia.",
            long_description=(
                "### Project Overview\n"
                "• Developed a Python-based machine learning application to analyze blood reports using OCR technology.\n"
                "• Extracted medical parameters from PDF and image-based reports.\n"
                "• Built predictive models to identify diseases such as anemia and leukemia.\n"
                "• Automated health analysis, reducing manual interpretation time.\n\n"
                "### Technical Details\n"
                "This application converts PDF document pages into image buffers using `pdf2image`, "
                "applies OpenCV binary threshold filters, extracts relevant metrics using Tesseract OCR, "
                "and performs classifications for anemia or leukemia risks."
            ),
            image="projects/blood_main.jpg",
            tech_stack="Python, Machine Learning, OCR, Data Processing",
            github_url="https://github.com/Sreesh-S/Smart-Blood-Report-Analyzer-Disease-Predictor",
            live_url="",
            is_featured=False,
            features=json.dumps([
                "Developed a Python-based machine learning application to analyze blood reports using OCR technology.",
                "Extracted medical parameters from PDF and image-based reports.",
                "Built predictive models to identify diseases such as anemia and leukemia.",
                "Automated health analysis, reducing manual interpretation time."
            ]),
            challenges=(
                "Resolving layout variance across different medical laboratories. "
                "We applied layout-agnostic regex pattern matching based on biomarker terminology rather than positional spacing."
            )
        )

        # Project 3: EV Charging
        p3 = Project.objects.create(
            title="EV Charging Station Locator",
            subtitle="Station Navigation Portal",
            description="Developed a web application to locate nearby EV charging stations with real-time availability and pricing details. Displayed connector information to improve accessibility and user convenience.",
            long_description=(
                "### Project Overview\n"
                "• Developed a web application to locate nearby EV charging stations with real-time availability and pricing details.\n"
                "• Displayed connector information to improve accessibility and user convenience.\n\n"
                "### Details\n"
                "Integrates map APIs to render station positions. Shows real-time port occupation status, charger plug models, "
                "and calculated route distances."
            ),
            image="projects/ev_main.jpg",
            tech_stack="HTML, CSS, JavaScript, Node.js, Database Integration",
            github_url="https://github.com/Sreesh-S/EV-Charging-Station-Locator",
            live_url="",
            is_featured=False,
            features=json.dumps([
                "Developed a web application to locate nearby EV charging stations with real-time availability and pricing details.",
                "Displayed connector information to improve accessibility and user convenience."
            ]),
            challenges=(
                "Rendering station cluster details smoothly. Resolved using Leaflet MarkerCluster configurations to group points dynamically."
            )
        )

        # Project 4: VKART Grocery
        p4 = Project.objects.create(
            title="VKART – Online Grocery Web Application",
            subtitle="Grocery E-Commerce Platform",
            description="Built an online grocery shopping platform with product listing, cart management, and order placement features. Enabled home delivery with clear pricing and product details for a seamless user experience.",
            long_description=(
                "### Project Overview\n"
                "• Built an online grocery shopping platform with product listing, cart management, and order placement features.\n"
                "• Enabled home delivery with clear pricing and product details for a seamless user experience.\n\n"
                "### Details\n"
                "A full stack shopping application utilizing session caches for cart persistence, order placement records in SQL, "
                "and stock inventory tables managed by admin panels."
            ),
            image="projects/vkart_main.jpg",
            tech_stack="HTML, CSS, JavaScript, PHP, MySQL",
            github_url="https://github.com/Sreesh-S/VKART-Online-Grocery-Web-Application",
            live_url="",
            is_featured=False,
            features=json.dumps([
                "Built an online grocery shopping platform with product listing, cart management, and order placement features.",
                "Enabled home delivery with clear pricing and product details for a seamless user experience."
            ]),
            challenges=(
                "Cart persistence. Combined JS localStorage backups with database tables to maintain cart synchronizations."
            )
        )

        # Project 5: Draupadi Saree E-Commerce
        p5 = Project.objects.create(
            title="Draupadi Saree E-Commerce Website",
            subtitle="Serverless Saree E-Commerce Platform",
            description="A premium serverless e-commerce application for traditional Indian wear (sarees). Built with React, Vite, and styled with custom CSS/TailwindCSS, using Supabase for authentication, real-time database transactions, and catalog storage.",
            long_description=(
                "### Project Overview\n"
                "• Designed and built a serverless e-commerce platform for sarees and traditional wear.\n"
                "• Integrates Supabase as the backend for database storage, real-time sync, and user authentication.\n"
                "• Features dynamic catalog filtering, shopping cart checkout flows, and transaction logs.\n"
                "• Developed a highly responsive user experience using React, Vite, and custom layouts.\n\n"
                "### Technical Implementation\n"
                "Vite powers fast hot-module loads, and Supabase JS clients process database queries without a custom intermediate server layer."
            ),
            image="projects/draupadi_main.jpg",
            tech_stack="React, JavaScript, Vite, Supabase, TailwindCSS, CSS3",
            github_url="https://github.com/Sreesh-S/draupadi-saree-ecommerce",
            live_url="",
            is_featured=False,
            features=json.dumps([
                "Real-time database sync using Supabase tables",
                "Fast serverless user registration and authentication",
                "Full interactive cart management and checkout flows",
                "Vite-optimized loading speeds and asset compilations"
            ]),
            challenges=(
                "Syncing cart state across local cache and database when connection is lost. "
                "Implemented optimistic UI updates combined with Supabase subscription channels to reconcile states on network reconnect."
            )
        )
        
        self.stdout.write('Seeded 5 projects.')

        # 4. Experience
        Experience.objects.all().delete()
        Experience.objects.create(
            company="Alpha Innovation Private Limited",
            role="Cyber Security Intern",
            start_date="January 2026",
            end_date="March 2026",
            achievements=json.dumps([
                "Gaining hands-on exposure to cybersecurity fundamentals, cyber threats, and basic defensive techniques.",
                "Assisting in security analysis and learning industry best practices in information security."
            ]),
            responsibilities=json.dumps([
                "Cybersecurity fundamentals review",
                "Assisting in security log analysis",
                "Information security research"
            ]),
            is_current=False,
            order=1
        )
        self.stdout.write('Seeded experiences.')

        # 5. Education
        Education.objects.all().delete()
        Education.objects.create(
            institution="Mangalam College of Engineering, Ettumanoor",
            degree="Master of Computer Applications (MCA)",
            field_of_study="Computer Applications",
            start_year="2024",
            end_year="2026",
            grade="Completed",
            description="Developing academic competency in Software Development, backend databases, machine learning systems, and project implementations.",
            order=1
        )
        Education.objects.create(
            institution="PG Radhakrishnan Memorial Sree Narayana College, Channanikadu",
            degree="Bachelor of Computer Applications (BCA)",
            field_of_study="Computer Applications",
            start_year="2021",
            end_year="2024",
            grade="Completed",
            description="Acquired core understandings of software principles, relational databases, structured programming in Python/Java/C, and web development fundamentals.",
            order=2
        )
        self.stdout.write('Seeded education.')

        # 6. Certifications
        Certification.objects.all().delete()
        Certification.objects.create(
            name="Cyber Security Internship",
            issuing_organization="Alpha Innovation",
            issue_date="March 2026",
            description="Completed Cyber Security internship at Alpha Innovation Private Limited, gaining hands-on experience in security fundamentals, threat analysis, and secure application practices.",
            credential_id="ALPHJAN-MAR228",
            hover_glow="#00F5FF"
        )
        Certification.objects.create(
            name="Web Development Training",
            issuing_organization="Nesote Technologies (P) Limited",
            issue_date="April 2024",
            description="Completed hands-on training in web development covering HTML, CSS, JavaScript, PHP, and MySQL, with focus on building dynamic and database-driven web applications.",
            hover_glow="#7B61FF"
        )
        Certification.objects.create(
            name="Microsoft Excel Using AI",
            issuing_organization="Office Master",
            issue_date="July 2025",
            description="Completed training on using AI-powered features in Microsoft Excel for data analysis, automation, and productivity enhancement.",
            hover_glow="#39FF14"
        )
        Certification.objects.create(
            name="Power BI Dashboard for Data Analytics",
            issuing_organization="WsCube Tech",
            issue_date="August 2025",
            description="Completed training on building interactive Power BI dashboards for data analytics, including data visualization, reporting, and insights generation.",
            hover_glow="#FFD600"
        )
        Certification.objects.create(
            name="GenAI for Data Analytics",
            issuing_organization="WsCube Tech",
            issue_date="July 2025",
            description="Completed a hands-on training on using Generative AI tools and techniques for data analytics tasks, including data understanding, analysis workflows, and productivity enhancement.",
            hover_glow="#FF9100"
        )
        Certification.objects.create(
            name="Foundation of Cloud IoT Edge ML",
            issuing_organization="NPTEL",
            issue_date="April 2025",
            description="Completed the NPTEL course “Foundation of Cloud IoT Edge ML” conducted by IIT Kanpur, covering cloud computing, IoT systems, edge computing, and machine learning concepts.",
            credential_id="NPTEL25CS75S449900311",
            hover_glow="#00E676"
        )
        Certification.objects.create(
            name="AI Tools & ChatGPT Workshop",
            issuing_organization="Be10x",
            issue_date="April 2025",
            description="Completed AI Tools & ChatGPT Workshop by Be10x, focusing on leveraging generative AI tools for productivity, content creation, and workflow automation.",
            hover_glow="#E040FB"
        )
        self.stdout.write('Seeded certifications.')

        # 7. Blog Posts
        Blog.objects.all().delete()
        Blog.objects.create(
            title="Getting Started with Machine Learning for Network Security",
            content=(
                "As network security threats evolve, static firewall rules are no longer sufficient to stop "
                "complex distributed attacks. By training machine learning models like Random Forests on standard datasets "
                "such as CICIDS2017, we can flag anomalous behavior with near 99% accuracy. In this guide, "
                "we discuss parsing network packets, compiling them into bidirectional flow metrics, and hooking model inference "
                "into a real-time web portal powered by Django."
            ),
            read_time=6
        )
        Blog.objects.create(
            title="Transforming Health Diagnostics: Building OCR Analyzers",
            content=(
                "Physical medical sheets and laboratory PDFs are hard to track and search. "
                "By leveraging Optical Character Recognition (OCR) with Python's Tesseract and image processing libraries like OpenCV, "
                "we can automatically extract medical biomarker values, check them against reference sheets, "
                "and predict potential wellness issues, allowing patients to track their personal health over time."
            ),
            read_time=5
        )
        self.stdout.write('Seeded blogs.')

        # 8. Social Links
        SocialLinks.objects.all().delete()
        SocialLinks.objects.create(platform="GitHub", url="https://github.com/Sreesh-S", icon_class="fa-brands fa-github")
        SocialLinks.objects.create(platform="LinkedIn", url="https://www.linkedin.com/in/s-sreesh", icon_class="fa-brands fa-linkedin")
        SocialLinks.objects.create(platform="Email", url="mailto:ssreesh45@gmail.com", icon_class="fa-solid fa-envelope")
        self.stdout.write('Seeded socials.')

        self.stdout.write(self.style.SUCCESS('Successfully seeded all portfolio database values!'))
