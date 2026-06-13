from llm import client

def classify_query(message):

    portfolio_keywords = [
            # projects / work
            "project",
            "portfolio",
            "work",
            "build",
            "built",
            "developed",
            "made",
            "created",
            "app",
            "application",
            "website",
            "tech stack",
            "github",
            "repo",
            "repository",
            "demo",
    
            # resume / experience
            "resume",
            "cv",
            "experience",
            "intern",
            "internship",
            "job",
            "career",
            "worked",
            "company",
            "role",
    
            # education
            "education",
            "degree",
            "study",
            "studied",
            "studying",
            "college",
            "university",
            "school",
            "major",
            "graduate",
            "graduation",
    
            # certifications / courses
            "certification",
            "certificate",
            "course",
            "training",
            "bootcamp",
            "learned",
            "qualification",
    
            # skills
            "skill",
            "tech",
            "technology",
            "language",
            "framework",
            "tool",
            "proficient",
            "good at",
            "know how to",
            "stack",
    
            # contact
            "contact",
            "email",
            "reach",
            "linkedin",
            "phone",
            "number",
            "social",
    
            # personal / about
            "about you",
            "about her",
            "about divya",
            "who is divya",
            "who are you",
            "tell me about",
            "background",
            "bio",
            "introduce",
            "yourself",
    
            # hobbies / interests / sidequests
            "hobby",
            "hobbies",
            "sidequest",
            "side quest",
            "side project",
            "interest",
            "passion",
            "free time",
            "spare time",
            "fun fact",
            "extracurricular",
            "activities",
            "achievement",
            "award",
    
            # specific personal interests
            "violin",
            "music",
            "sport",
            "sports",
            "art",
            "literature",
            "reading",
            "gaming",
            "game",
    
            # name
            "divya",
            "divyasree",
        ]

    msg = message.lower()

    # FAST PATH
    for word in portfolio_keywords:
        if word in msg:
            print("KEYWORD ROUTER HIT")
            return "portfolio"

    # LLM FALLBACK
    print("LLM ROUTER")

    prompt = f"""
Classify this query into exactly one category.

Categories:

portfolio
- Questions about Divyasree
- Projects
- Skills
- Experience
- Education
- Certifications
- Contact information
- Resume
- Personal background
- Interests and extracurriculars

writer
- Story writing
- Character creation
- Plot analysis
- Worldbuilding
- Research
- Creative brainstorming

Query:
{message}

Respond with ONLY:

portfolio

or

writer
"""

    try:
        response = client.chat.completions.create(
            model="deepseek/deepseek-chat-v3",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )

        result = (
            response.choices[0].message.content or ""
        ).strip().lower()

        if result in ["portfolio", "writer"]:
            return result

    except Exception as e:
        print("Router error:", e)

    # Safe fallback
    return "writer"