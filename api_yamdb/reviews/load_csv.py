from csv import DictReader

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import User


def import_csv_data():
    csv_files = (
        (User, 'data/users.csv'),
        (Category, 'data/category.csv'),
        (Genre, 'data/genre.csv'),
        (Title, 'data/titles.csv'),
        (GenreTitle, 'data/genre_title.csv'),
        (Review, 'data/review.csv'),
        (Comment, 'data/comments.csv')
    )

    for model, file in csv_files:
        print(f"Загрузка данных таблицы {file} началась.")
        for row in DictReader(open(file, encoding='utf-8')):
            if file == 'data/users.csv':
                data = model(
                    id=row['id'],
                    username=row['username'],
                    email=row['email'],
                    role=row['role'],
                    bio=row['bio'],
                    first_name=row['first_name'],
                    last_name=row['last_name']
                )
                data.save()
            elif file in ['data/category.csv', 'data/genre.csv']:
                data = model(
                    id=row['id'],
                    name=row['name'],
                    slug=row['slug']
                )
                data.save()
            elif file == 'data/titles.csv':
                data = model(
                    id=row['id'],
                    name=row['name'],
                    year=row['year'],
                    category_id=row['category_id']
                )
                data.save()
            elif file == 'data/genre_title.csv':
                data = model(
                    id=row['id'],
                    title_id=row['title_id'],
                    genre_id=row['genre_id']
                )
                data.save()
            elif file == 'data/review.csv':
                data = model(
                    id=row['id'],
                    title_id=row['title_id'],
                    text=row['text'],
                    author_id=row['author'],
                    score=row['score'],
                    pub_date=row['pub_date']
                )
                data.save()
            elif file == 'data/comments.csv':
                data = model(
                    id=row['id'],
                    review_id=row['review_id'],
                    text=row['text'],
                    author_id=row['author'],
                    pub_date=row['pub_date']
                )
                data.save()
        print(
            f"Загрузка данных из {file} завершена успешно.")


def main():
    try:
        import_csv_data()
    except Exception as error:
        print(f"Сбой в работе импорта: {error}.")
    finally:
        print("Завершена работа импорта.")


if __name__ == '__main__':
    main()
