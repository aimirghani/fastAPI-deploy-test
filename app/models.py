from sqlalchemy import Column, text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from app.database import Base



class Post(Base):
    __tablename__ = "posts"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    content: Mapped[str] = mapped_column(nullable=False)
    published: Mapped[bool] = mapped_column(nullable=False, server_default=text("TRUE"))
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text("now()"))
    owner_id: Mapped[bool] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), 
                                            nullable=False)
    owner: Mapped["User"] = Relationship(back_populates="posts")


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, 
                        server_default=text("now()"))
    posts: Mapped[list["Post"]] = Relationship(back_populates="owner")


class Vote(Base):
    __tablename__ = "votes"
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), 
                                        primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), 
                                        primary_key=True)