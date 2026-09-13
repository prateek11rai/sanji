---
title: Résumé
# EDIT ON ROLE CHANGE. Becomes the meta description and the llms.txt entry,
# so it states the current title and employer. One sentence, plus "Previously
# <employer>" once there is more than one worth naming.
description: Senior Software Engineer at Atlan, building data connectivity and platform services. Previously BYJU'S.
hide:
  - feedback
---

<!-- APPEND = add entries, don't rewrite. FROZEN = historical, only fix
     errors. llms.txt, the JSON-LD and the meta description are generated
     from this file and mkdocs.yml — never hand-edit them. -->

# Prateek Rai

<!-- APPEND: one link per line. Icons come from mkdocs' custom_icons. These
     are NOT the footer socials — those live in extra.social. The first entry
     is where you live: edit the label and the maps URL if that changes. -->
<div class="resume-contact" markdown="span">
[:material-map-marker: Kolkata, India](https://www.google.com/maps/place/Kolkata,+West+Bengal,+India)
[:fontawesome-brands-linkedin: LinkedIn](https://www.linkedin.com/in/prateek11rai/)
[:fontawesome-brands-github: GitHub](https://github.com/prateek11rai)
[:fontawesome-solid-envelope: prateek11rai@protonmail.com](mailto:prateek11rai@protonmail.com)
</div>

<!-- The positioning line. Rarely changes — it outlives any one job. -->
I build data platforms that scale — and I use LLMs to do it faster.

<!-- EDIT ON ROLE CHANGE: title and employer. Said in three other places —
     `description:` above, and `extra.person.jobTitle` / `worksFor` in
     mkdocs.yml. All four have to agree. -->
Senior Software Engineer at [Atlan](https://atlan.com), working on the metadata catalog that helps Fortune 500 enterprises understand and govern their data. My work sits at the intersection of distributed systems, data infrastructure and AI-augmented engineering.

<!-- APPEND: newest employer first, newest role first within each employer.
     Company is `###` + location; each role is `####` + date range + an
     optional one-line summary + bullets. -->
## Experience

### [Atlan](https://atlan.com)

*Remote*

<!-- EDIT ON ROLE CHANGE: on promotion add the new role ABOVE this one and
     close this date range at the month. Don't overwrite the title — the old
     one is what shows the progression. Then update extra.person.jobTitle in
     mkdocs.yml. New employer: a new `###` block above Atlan, and worksFor. -->
#### Senior Software Engineer I

*Mar 2026 – Present*

Architecting and building the next generation of data connectivity and platform services for Atlan's metadata catalog.

- Re-architected a high-traffic enterprise connector from Argo to Temporal on a next-generation SDK, cutting peak memory by 13x and eliminating recurring out-of-memory failures through streaming extraction and chunk-wise enrichment.
- Led the design of reusable intermediary services and SDK components for partner integrations, creating a generic ingestion pipeline and standardised asset model adopted by 10+ engineering teams.
- Drove end-to-end resolution for 300+ high-impact customer issues across 25+ Fortune 500 enterprises.
- Shipped 5+ joint catalog and lineage integrations from preview to general availability through cross-functional collaboration.

<!-- FROZEN -->
#### Data Engineer

*Apr 2024 – Mar 2026*

Built and delivered core data-source connectors for Atlan's metadata catalog.

- Designed and shipped multiple production connectors and platform services, owning architecture, implementation and release end-to-end.
- Developed ingestion pipelines and reusable integration components adopted by downstream engineering teams.
- Drove resolution for customer issues across enterprise accounts, working cross-functionally with engineering and partner teams.

<!-- FROZEN: everything from here to the end of Experience. -->
### [BYJU'S](https://byjus.com)

*Bangalore, Karnataka*

#### Member of Technical Staff I

*Oct 2023 – Apr 2024*

- Engineered OLAP pipelines, introducing event triggers for real-time JSON delivery and orchestrating scheduled jobs on Apache Airflow alongside OLTP pipelines on Kafka Connect.
- Owned and optimised ETL pipelines with Talend and AWS Glue, holding a 95% success rate on bulk-load jobs, and managed the Snowflake warehouse with Python/SQL tasks, complex role structures and data masking.
- Spearheaded an Apache Superset implementation for dynamic dashboarding, cutting Snowflake credit usage by 10% through a query and cost monitoring dashboard on a Dockerised EC2 deployment.

#### Engineering Intern

*Jan 2023 – Sep 2023*

- Engineered Spark-based data transfer utilities handling 10+ TB and 100M+ records across Parquet, CSV and JSON.
- Streamlined Spark job creation across 30+ data pipelines using AWS Glue, and improved data accessibility for 50+ datasets through AWS Athena.
- Worked on the Snowflake warehouse with Python for data processing and automation, reducing processing errors by 40% across 20+ sources.

<!-- APPEND, sparingly. Six groups, ~30 items total — it's curated, not a
     dump of the LinkedIn list. Adding a line means dropping one. Order
     within a group is rough priority, not alphabetical. -->
## Skills

**Core** — Systems Design, Software Architecture, Distributed Systems, Microservices

**Languages** — Python, Go, SQL, TypeScript

**Platform** — Temporal, Argo Workflows, Apache Airflow, Kafka, Kubernetes, Docker, Terraform, FastAPI

**Data** — Snowflake, BigQuery, PostgreSQL, Apache Iceberg, Apache Atlas, Elasticsearch, Spark

**Cloud** — AWS, GCP, Azure

**AI engineering** — LLM agents, Model Context Protocol, context engineering, Claude Agent SDK

<!-- APPEND: newest first. Heading is the project, linked to its page under
     docs/projects/ when it has one. Then the date (right-aligns onto the
     heading), then a line for the repo, then bullets — same shape as
     Experience and Education. Bullets carry what was built and the numbers;
     the long version lives on the project page, not here. -->
## Projects

### [DocAid](projects/doc-aid/index.md)

*Jan 2022 – Jan 2023*

*[GitHub](https://github.com/prateek11rai/DocAid) · Capstone project, Thapar University*

- Engineered an IoT wearable on Arduino Uno with pulse, oxygen, temperature and ECG sensors, streaming 100 readings/min to a Firebase realtime database.
- Built a real-time Django/Channels dashboard monitoring up to 500 patients.

### GitRep Scorer

*Jun 2022 – Jul 2022*

*[GitHub](https://github.com/prateek11rai/Gitrep_Scorer)*

- Built a GitHub repository rating tool in Python, scoring a 10,000-repo Kaggle dataset with BeautifulSoup and TOPSIS analysis.
- Deployed as a Streamlit app.

<!-- CERTIFICATIONS — commented out until there is something worth listing.

     The bar: an independent credential with an exam behind it and a public
     verification URL (AWS/GCP professional, CKA, Temporal, and so on). Course
     completions do not clear it — at this level they read as weaker evidence
     than the work already described above, and LinkedIn is where the
     exhaustive list belongs.

     Shape mirrors Education: heading is the credential, the first italic line
     is the date (it right-aligns onto the heading automatically), the second
     is issuer and verification link. Newest first. Uncomment the heading too.

## Certifications

### Credential name

*Month Year*

*Issuer · [Verify](https://credential-url)*

-->

<!-- APPEND: newest first, one block per qualification — not per school, so a
     school with two qualifications appears twice. Heading is the qualification;
     the italic line is institution, place and completion date; bullets carry
     grade first, then anything worth adding (honours, thesis, coursework).
     If a new qualification goes on top, update extra.person.alumniOf in
     mkdocs.yml to match it. -->
## Education

### BE, Computer Science and Engineering

*June 2023*

*[Thapar Institute of Engineering and Technology](https://www.thapar.edu) · Patiala, Punjab*

- CGPA: 8.84
- Minor: Data Science

### Class 12, CBSE

*June 2018*

*[Army Public School](https://apsambala.edu.in/) · Ambala Cantt, Haryana*

- Percentage: 94.2%
- Subjects: Physics, Chemistry and Mathematics, with English and Information Technology

### Class 10, CBSE

*June 2016*

*[Army Public School](https://apsambala.edu.in/) · Ambala Cantt, Haryana*

- CGPA: 10
