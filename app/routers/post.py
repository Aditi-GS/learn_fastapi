from fastapi import status, HTTPException, Depends, APIRouter, Response
from typing import List, Optional
from ..models import Post, Vote
from ..schemas import User, PostCreate, PostResponse, PostUpdate, PostWithVotesResponse
from ..database import get_db
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_post = Post(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)    # == RETURNING * in SQL
    return  new_post

@router.get("/", response_model=List[PostWithVotesResponse])
def get_all_posts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user),
                  limit: int = 5, offset: int = 0, sort: str = "desc", title_contains: Optional[str] = ""):
       
    posts_query = db.query(Post, func.count(Vote.post_id).label("votes"))\
                .join(Vote, Post.id == Vote.post_id, isouter=True)\
                .group_by(Post.id)\
                .filter(
                    Post.user_id == current_user.id,\
                    Post.title.contains(title_contains)
                )

    if sort == "asc":
        posts_query = posts_query.order_by(Post.id.asc())
    else:
        posts_query = posts_query.order_by(Post.id.desc())

    posts = posts_query.limit(limit).offset(offset).all()        

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Table so empty T_T")

    return posts

@router.get("/latest", response_model=PostWithVotesResponse)
def get_latest_post(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.user_id == current_user.id).order_by(Post.created_at.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail="Table so empty T_T")
    result = db.query(Post, func.count(Vote.post_id).label("votes"))\
        .join(Vote, Post.id == Vote.post_id, isouter=True)\
        .group_by(Post.id)\
        .filter(Post.user_id == current_user.id)\
        .order_by(Post.created_at.desc()).first()
    return result

@router.get("/{id}", response_model=PostWithVotesResponse)
def get_post_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == id).one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Don't over-step your boundaries, buddy !")  
    result = db.query(Post, func.count(Vote.post_id).label("votes"))\
        .join(Vote, Post.id == Vote.post_id, isouter=True)\
        .group_by(Post.id)\
        .filter(Post.id == id).one_or_none() 
    return result

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !") 
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Don't over-step your boundaries, buddy !")    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post_by_id(id: int, updated_post: PostUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    post_query = db.query(Post).filter(Post.id == id)
    post = post_query.one_or_none()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Yo post {id} doesn't exist man !") 
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Don't over-step your boundaries, buddy !")        
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.one()