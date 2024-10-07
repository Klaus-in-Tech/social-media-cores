from fastapi import Depends, HTTPException, status, Response, APIRouter
from typing import List
from sqlalchemy.orm import Session
from .. import database_models, database, schemas, oauth2

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.Post])
async def get_posts(
    db: Session = Depends(database.get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    my_posts = db.query(database_models.Posts).all()
    return my_posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(
    post: schemas.CreatePost,
    db: Session = Depends(database.get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    # post_dic = post.dict()
    # post_dic['id'] = randrange(0,10000)
    # my_posts.append(post_dic)
    new_post = database_models.Posts(owner_id=curr_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}")
def get_post(
    id: int,
    db: Session = Depends(database.get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    # print(id)
    # post = find_post(id)

    post = (
        db.query(database_models.Posts).filter(database_models.Posts.id == id).first()
    )
    print(post)

    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found.",
        )
    return {"post details": post}


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    db: Session = Depends(database.get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    # index = find_index_post(id)
    post_query = db.query(database_models.Posts).filter(database_models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist",
        )

    if post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform the requested action",
        )

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}")
def update_post(
    id: int,
    updated_post: schemas.CreatePost,
    db: Session = Depends(database.get_db),
    curr_user: int = Depends(oauth2.get_current_user),
):
    # index = find_index_post(id)

    post_query = db.query(database_models.Posts).filter(database_models.Posts.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )

    if post.owner_id != curr_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorised to perform the requested action",
        )

    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    # my_posts[index] = post_dict
    # print(post)
    return post_query.first()
