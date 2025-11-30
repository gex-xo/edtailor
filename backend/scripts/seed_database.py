#!/usr/bin/env python3
"""
Seed script to populate EdTailor database with educational content.

Run from backend directory:
    python scripts/seed_database.py
"""

import sys
import os
import json
import asyncio
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import select

from app.core.config import settings
from app.core.database import Base
from app.models import Category, Topic, Lesson, Fabric, Garment, Term, Tag


# Color output for terminal
class Colors:
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_success(message):
    print(f"{Colors.GREEN}✓{Colors.END} {message}")


def print_info(message):
    print(f"{Colors.BLUE}ℹ{Colors.END} {message}")


def print_warning(message):
    print(f"{Colors.YELLOW}⚠{Colors.END} {message}")


def print_error(message):
    print(f"{Colors.RED}✗{Colors.END} {message}")


def load_json_file(filepath):
    """Load and parse JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print_error(f"File not found: {filepath}")
        return None
    except json.JSONDecodeError as e:
        print_error(f"Invalid JSON in {filepath}: {e}")
        return None


async def seed_categories_and_content(session: AsyncSession):
    """Seed English categories, topics, and lessons."""
    print_info("Loading educational content...")
    data = load_json_file('scripts/seed_data/educational_content.json')
    if data:
        await seed_categories_and_content_from_data(session, data)


async def seed_fabrics(session: AsyncSession):
    """Seed English fabric library."""
    print_info("Loading fabrics...")
    data = load_json_file('scripts/seed_data/fabrics.json')
    if data:
        await seed_fabrics_from_data(session, data)


async def seed_garments(session: AsyncSession):
    """Seed English garment encyclopedia."""
    print_info("Loading garments...")
    data = load_json_file('scripts/seed_data/garments.json')
    if data:
        await seed_garments_from_data(session, data)


async def seed_terms(session: AsyncSession):
    """Seed English terminology glossary."""
    print_info("Loading terms...")
    data = load_json_file('scripts/seed_data/terms.json')
    if data:
        await seed_terms_from_data(session, data)


async def seed_all_languages(session: AsyncSession):
    """Seed data for all available languages."""
    # English content
    print(f"\n{Colors.BOLD}=== Seeding English Content ==={Colors.END}\n")
    await seed_categories_and_content(session)
    await seed_fabrics(session)
    await seed_garments(session)
    await seed_terms(session)

    # Russian content
    print(f"\n{Colors.BOLD}=== Seeding Russian Content (Русский контент) ==={Colors.END}\n")
    await seed_categories_and_content_ru(session)
    await seed_fabrics_ru(session)
    await seed_garments_ru(session)
    await seed_terms_ru(session)


async def seed_categories_and_content_ru(session: AsyncSession):
    """Seed Russian categories, topics, and lessons."""
    print_info("Loading Russian educational content...")
    data = load_json_file('scripts/seed_data/educational_content_ru.json')
    if data:
        await seed_categories_and_content_from_data(session, data)


async def seed_fabrics_ru(session: AsyncSession):
    """Seed Russian fabric library."""
    print_info("Loading Russian fabrics...")
    data = load_json_file('scripts/seed_data/fabrics_ru.json')
    if data:
        await seed_fabrics_from_data(session, data)


async def seed_garments_ru(session: AsyncSession):
    """Seed Russian garment encyclopedia."""
    print_info("Loading Russian garments...")
    data = load_json_file('scripts/seed_data/garments_ru.json')
    if data:
        await seed_garments_from_data(session, data)


async def seed_terms_ru(session: AsyncSession):
    """Seed Russian terminology glossary."""
    print_info("Loading Russian terms...")
    data = load_json_file('scripts/seed_data/terms_ru.json')
    if data:
        await seed_terms_from_data(session, data)


async def seed_categories_and_content_from_data(session: AsyncSession, data: dict):
    """Seed categories, topics, and lessons from provided data."""
    category_map = {}

    for cat_data in data['categories']:
        result = await session.execute(
            select(Category).where(Category.slug == cat_data['slug'])
        )
        category = result.scalar_one_or_none()

        if category:
            print_warning(f"Category '{cat_data['name']}' already exists, skipping")
        else:
            category = Category(**cat_data)
            session.add(category)
            await session.flush()
            print_success(f"Created category: {cat_data['name']}")

        category_map[cat_data['slug']] = category

    await session.commit()

    topic_map = {}
    for topic_data in data['topics']:
        category_slug = topic_data.pop('category_slug')
        category = category_map.get(category_slug)

        if not category:
            print_error(f"Category not found for slug: {category_slug}")
            continue

        result = await session.execute(
            select(Topic).where(Topic.slug == topic_data['slug'])
        )
        topic = result.scalar_one_or_none()

        if topic:
            print_warning(f"Topic '{topic_data['name']}' already exists, skipping")
        else:
            topic = Topic(**topic_data, category_id=category.id)
            session.add(topic)
            await session.flush()
            print_success(f"Created topic: {topic_data['name']}")

        topic_map[topic_data['slug']] = topic

    await session.commit()

    for lesson_data in data['lessons']:
        topic_slug = lesson_data.pop('topic_slug')
        topic = topic_map.get(topic_slug)

        if not topic:
            print_error(f"Topic not found for slug: {topic_slug}")
            continue

        result = await session.execute(
            select(Lesson).where(Lesson.slug == lesson_data['slug'])
        )
        lesson = result.scalar_one_or_none()

        if lesson:
            print_warning(f"Lesson '{lesson_data['title']}' already exists, skipping")
        else:
            lesson = Lesson(**lesson_data, topic_id=topic.id)
            session.add(lesson)
            print_success(f"Created lesson: {lesson_data['title']}")

    await session.commit()


async def seed_fabrics_from_data(session: AsyncSession, data: dict):
    """Seed fabrics from provided data."""
    count = 0
    for fabric_data in data['fabrics']:
        result = await session.execute(
            select(Fabric).where(
                (Fabric.name == fabric_data['name']) &
                (Fabric.language == fabric_data.get('language', 'en'))
            )
        )
        fabric = result.scalar_one_or_none()

        if fabric:
            print_warning(f"Fabric '{fabric_data['name']}' already exists, skipping")
        else:
            fabric = Fabric(**fabric_data)
            session.add(fabric)
            count += 1
            print_success(f"Created fabric: {fabric_data['name']}")

    await session.commit()
    print_success(f"✓ Created {count} fabrics")


async def seed_garments_from_data(session: AsyncSession, data: dict):
    """Seed garments from provided data."""
    count = 0
    for garment_data in data['garments']:
        result = await session.execute(
            select(Garment).where(
                (Garment.name == garment_data['name']) &
                (Garment.language == garment_data.get('language', 'en'))
            )
        )
        garment = result.scalar_one_or_none()

        if garment:
            print_warning(f"Garment '{garment_data['name']}' already exists, skipping")
        else:
            garment = Garment(**garment_data)
            session.add(garment)
            count += 1
            print_success(f"Created garment: {garment_data['name']}")

    await session.commit()
    print_success(f"✓ Created {count} garments")


async def seed_terms_from_data(session: AsyncSession, data: dict):
    """Seed terms from provided data."""
    count = 0
    for term_data in data['terms']:
        result = await session.execute(
            select(Term).where(
                (Term.term == term_data['term']) &
                (Term.language == term_data.get('language', 'en'))
            )
        )
        term = result.scalar_one_or_none()

        if term:
            print_warning(f"Term '{term_data['term']}' already exists, skipping")
        else:
            term = Term(**term_data)
            session.add(term)
            count += 1
            print_success(f"Created term: {term_data['term']}")

    await session.commit()
    print_success(f"✓ Created {count} terms")


async def main():
    """Main seeding function."""
    print(f"\n{Colors.BOLD}=== EdTailor Database Seeding ==={Colors.END}\n")

    # Create async engine and session
    engine = create_async_engine(settings.database_url, echo=False)
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    try:
        async with async_session_maker() as session:
            # Seed all data in both languages
            await seed_all_languages(session)

            print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Database seeding completed successfully!{Colors.END}\n")
            print(f"{Colors.BLUE}📚 Content available in English and Russian (Английский и Русский){Colors.END}\n")

    except Exception as e:
        print_error(f"Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
