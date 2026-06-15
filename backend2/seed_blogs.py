import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import BlogPost, PostStatus
from app.database import Base

DATABASE_URL = "mysql+pymysql://root:1234@127.0.0.1:3306/hh"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_blogs():
    db = SessionLocal()
    try:
        new_posts = [
            BlogPost(
                title="The Ancient Art of Forest Bathing",
                slug="ancient-art-forest-bathing",
                content="Forest bathing, or Shinrin-yoku, is the simple method of being calm and quiet amongst the trees. It’s an opportunity to observe nature and breathe deeply. We infuse this philosophy into our earthy, grounding shampoos to help you recreate the forest experience at home.",
                seo_keyword="forest bathing",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Harnessing the Power of Aloe Vera",
                slug="harnessing-power-aloe-vera",
                content="Aloe vera has been used for centuries to heal and soothe the skin. In hair care, it provides deep hydration and enzymatic action that stimulates hair growth. Discover why our Botanical Aloe Mask is a cult favorite among those with dry scalps.",
                seo_keyword="aloe vera hair care",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Why Sulfates Belong in the Past",
                slug="why-sulfates-belong-in-past",
                content="Sulfates create satisfying lather, but at what cost? They strip the hair of its natural oils, leading to frizz and scalp irritation. Learn how our sulfate-free cleansers use coconut-derived surfactants to clean without compromising your hair's barrier.",
                seo_keyword="sulfate free shampoo",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="The Secret to Shiny Hair: Fermented Rice Water",
                slug="secret-shiny-hair-fermented-rice-water",
                content="An ancient Yao women tradition, fermented rice water is rich in inositol, a carbohydrate that repairs damaged hair from the inside out. Our Fermented Rice Essence is designed to give you that glass-hair shine naturally.",
                seo_keyword="fermented rice water",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Understanding Scalp Microbiome",
                slug="understanding-scalp-microbiome",
                content="Your scalp is an ecosystem. Over-washing and harsh chemicals disrupt the microbiome, leading to dandruff and oil overproduction. Explore how Verdant Mane’s Prebiotic Scalp Serum feeds the good bacteria for a healthy foundation.",
                seo_keyword="scalp microbiome",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Rosemary Oil: Nature's Minoxidil?",
                slug="rosemary-oil-natures-minoxidil",
                content="Recent studies suggest rosemary oil can be as effective as standard hair loss treatments, without the itching. We break down the science and show you how to properly dilute and apply our pure Rosemary Essential Oil for maximum growth.",
                seo_keyword="rosemary oil hair growth",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Detoxifying With Bentonite Clay",
                slug="detoxifying-with-bentonite-clay",
                content="Product buildup weighs your hair down. Bentonite clay acts like a magnet, drawing out impurities and heavy metals from your strands. Read our guide on how to perform a monthly clay detox for lighter, bouncier hair.",
                seo_keyword="bentonite clay hair detox",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="Seasonal Hair Care Transitions",
                slug="seasonal-hair-care-transitions",
                content="As the weather changes, so should your hair routine. Winter calls for heavy moisture, while summer demands UV protection. Learn how to adapt your Verdant Mane regimen to keep your hair thriving year-round.",
                seo_keyword="seasonal hair care",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="The Myth of Healing Split Ends",
                slug="myth-of-healing-split-ends",
                content="Many products claim to heal split ends, but the truth is, once the structural integrity is compromised, a trim is the only cure. However, you can prevent them. Uncover our tips for strengthening the hair cuticle using Argan and Jojoba oils.",
                seo_keyword="prevent split ends",
                status=PostStatus.published,
                created_by=6
            ),
            BlogPost(
                title="A Guide to Ethical Botanical Sourcing",
                slug="guide-ethical-botanical-sourcing",
                content="How do we ensure our ingredients don't harm the earth? From our fair-trade Shea Butter cooperatives in Ghana to our sustainable Lavender farms in France, we trace every leaf. Transparency is our promise to you.",
                seo_keyword="ethical sourcing",
                status=PostStatus.published,
                created_by=6
            ),
        ]
        
        # Check if they exist to prevent duplicates
        existing_slugs = [p.slug for p in db.query(BlogPost).all()]
        added = 0
        for post in new_posts:
            if post.slug not in existing_slugs:
                db.add(post)
                added += 1
                
        db.commit()
        print(f"Successfully added {added} new blog posts.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_blogs()
