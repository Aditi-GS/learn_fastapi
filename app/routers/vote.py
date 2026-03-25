from fastapi import APIRouter, status, Depends, HTTPException
from ..database import get_db
from ..oauth2 import get_current_user
from .. import schemas
from ..models import Vote, Post
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    # Check if post exists -> Check if user already voted -> Add/Remove Vote
    post = db.query(Post).filter(Post.id == vote.post_id).one_or_none()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # prevent self-voting
    # if post.user_id == current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Come on, you can't vote your own post")

    vote_query = db.query(Vote).filter(
        Vote.post_id == vote.post_id,
        Vote.user_id == current_user.id
    )
    is_voted = vote_query.one_or_none()

    if vote.dir == 1:
        if is_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User {current_user.id} has already liked post {vote.post_id}")
        new_vote = Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"message": "Vote Added !"}
    else:
        if not is_voted:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Vote doesn't exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote Deleted !"}

