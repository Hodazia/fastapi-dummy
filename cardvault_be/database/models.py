from sqlalchemy import String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from database.base import Base 

'''
a user can create many content
1-many relationship , 1 User- >Many contents

the DB doesn't need to store , user -> Content objects , instead it stores a foreign key, 
users

id | username
---|---------
1  | zia
2  | john

contents

id | title      | user_id
---|------------|--------
10 | FastAPI    | 1
11 | SQLAlchemy | 1
12 | JWT        | 1
13 | React      | 2

Notice contents.user_id contains 1 1 1 2
this is how the DB nows
Content 10 → User 1
Content 11 → User 1
Content 12 → User 1
Content 13 → User 2


'''

class User(Base):
    __tablename__="users"
    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )
    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    hashed_password: Mapped[str]= mapped_column(
        String(255),
        nullable=False
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    # a user can have many Contents and hence there is a list
    contents: Mapped[list["Content"]] = relationship(
        back_populates="user"
    )
    link: Mapped["Link | None"] = relationship(
    back_populates="user",
    uselist=False
)

class Content(Base):
    __tablename__ = "contents"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    link: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    type: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    # each content can have only 1 user
    user: Mapped["User"] = relationship(
        back_populates="contents"
    )

    tags: Mapped[list["Tag"]] = relationship(
        secondary="content_tags",
        back_populates="contents"
    )

'''
users.id
   ▲
   │
   │ ForeignKey
   │
contents.user_id

if u do user.contents, it returns
[
    Content(id=10, title="FastAPI"),
    Content(id=11, title="JWT")
]
and content.user returns
User(id=1, username="zia")

Why does Content have user_id? bcz the foreign key belongs on the many side
the content table needs to remember which user owns me?
: user_id = ForeignKey("users.id")
'''

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    contents: Mapped[list["Content"]] = relationship(
        secondary="content_tags",
        back_populates="tags"
    )

'''
content_tags

content_id | tag_id
-----------|-------
1          | 10
1          | 20
1          | 30
2          | 10
2          | 40

Content 1
 ├── Tag 10
 ├── Tag 20
 └── Tag 30

Content 2
 ├── Tag 10
 └── Tag 40


 

'''
class ContentTag(Base):
    __tablename__ = "content_tags"

    content_id: Mapped[int] = mapped_column(
        ForeignKey("contents.id", ondelete="CASCADE"),
        primary_key=True
    )

    tag_id: Mapped[int] = mapped_column(
        ForeignKey("tags.id", ondelete="CASCADE"),
        primary_key=True
    )

class Link(Base):
    __tablename__ = "links"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        unique=True,
        nullable=False,
        index=True
    )

    user: Mapped["User"] = relationship(
        back_populates="link"
    )