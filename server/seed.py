#!/usr/bin/env python3

from random import randint, choice as rc
from faker import Faker

from app import app
from models import db, Article, User

fake = Faker()

with app.app_context():
    print("Deleting all records...")
    Article.query.delete()
    User.query.delete()

    print("Creating users...")
    users = []
    usernames = []

    # ✅ Always ensure at least one test user exists
    test_user = User(username="testuser")
    users.append(test_user)

    # Generate extra random users
    for i in range(24):
        username = fake.first_name()
        while username in usernames or username == "testuser":
            username = fake.first_name()

        usernames.append(username)
        user = User(username=username)
        users.append(user)

    db.session.add_all(users)

    print("Creating articles...")
    articles = []

    # ✅ Always create at least one public and one member-only article
    public_article = Article(
        author="Admin",
        title="Public Post",
        content="This article is visible to everyone.",
        preview="Public article...",
        minutes_to_read=5,
        is_member_only=False
    )

    member_article = Article(
        author="Admin",
        title="Private Post",
        content="This article is only for members.",
        preview="Private article...",
        minutes_to_read=7,
        is_member_only=True
    )

    articles.extend([public_article, member_article])

    # Generate extra random articles
    for i in range(98):
        content = fake.paragraph(nb_sentences=8)
        preview = content[:25] + '...'

        article = Article(
            author=fake.name(),
            title=fake.sentence(),
            content=content,
            preview=preview,
            minutes_to_read=randint(1, 20),
            is_member_only=rc([True, False, False])
        )

        articles.append(article)

    db.session.add_all(articles)

    db.session.commit()
    print("Seeding complete ✅")
