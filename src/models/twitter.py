from typica import BaseModel, Optional, Field, Any
from typica.utils.enums import EnumV2


class RequestSchema(BaseModel):
    uri: str
    params: Optional[dict] = Field({})
    date: str


class FollowMeta(BaseModel):
    user_id: str
    name: str
    screen_name: str
    description: Optional[str] = Field("")
    profile_image: Optional[str] = Field("")
    statuses_count: Optional[int] = Field(0)
    followers_count: Optional[int] = Field(0)
    friends_count: Optional[int] = Field(0)
    media_count: Optional[int] = Field(0)


class FollowingMeta(BaseModel):
    following: Optional[list[FollowMeta]] = Field([])
    next_cursor: Optional[str] = Field(None)


class FollowerMeta(BaseModel):
    followers: Optional[list[FollowMeta]] = Field([])
    next_cursor: Optional[str] = Field(None)
    followers_count: int
    status: str


class TimelineMeta(BaseModel):
    tweet_id: str
    screen_name: Optional[str] = Field("")
    text: Optional[str] = ""
    lang: Optional[str] = "und"
    quotes: Optional[int] = Field(0)
    replies: Optional[int] = Field(0)
    retweets: Optional[int] = Field(0)
    bookmarks: Optional[int] = Field(0)
    favorites: Optional[int] = Field(0)
    created_at: Optional[str] = ""


class UserMeta(BaseModel):
    id: str
    profile: str
    rest_id: str
    avatar: Optional[str] = Field("")
    desc: Optional[str] = Field("")
    name: str
    friends: Optional[int] = Field(0)
    sub_count: Optional[int] = Field(0)


class Search(BaseModel):
    timeline: Optional[list[TimelineMeta]] = Field([])
    next_cursor: Optional[str] = Field(None)


class Timeline(BaseModel):
    timeline: Optional[list[TimelineMeta]] = Field([])
    user: UserMeta
