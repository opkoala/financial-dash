import socket
import json
import datetime
from sqlalchemy import create_engine, Column, Integer, Date, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy setup
Base = declarative_base()

class ReviewSchedule(Base):
    __tablename__ = 'review_schedule'
    id = Column(Integer, primary_key=True)
    review_id = Column(String, unique=True)
    review_date = Column(Date)

# Database setup
engine = create_engine('sqlite:///reviews.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


# Socket setupx
HOST = '127.0.0.1'
PORT = 65432

def get_review_date(increment_days=60):
    # Provide default increment_days if None is passed
    if increment_days is None:
        increment_days = 60  # Default value if not provided
    today = datetime.date.today()
    return today + datetime.timedelta(days=increment_days)

def check_for_conflict(session, review_date):
    return session.query(ReviewSchedule).filter(ReviewSchedule.review_date == review_date).count() > 0

def handle_client_connection(conn):
    try:
        # Receive data from the client
        data = conn.recv(1024).decode()
        if not data:
            return

        request = json.loads(data)
        review_id = request['id']
        increment = request.get('increment', 60)  # Default to 60 if not provided

        # Determine the review date
        review_date = get_review_date(increment)

        # Open session to interact with the database
        session = Session()

        # Check if the review date is available, otherwise increment until free
        while check_for_conflict(session, review_date):
            review_date += datetime.timedelta(days=1)

        # Add the review to the database
        new_review = ReviewSchedule(review_id=review_id, review_date=review_date)
        session.add(new_review)
        session.commit()

        # Fetch the entire database
        reviews = session.query(ReviewSchedule).all()
        reviews_data = [{'id': review.review_id, 'review_date': review.review_date.isoformat()} for review in reviews]

        # Send the entire database back to the client
        conn.sendall(json.dumps(reviews_data).encode())
    finally:
        conn.close()

def start_server():
    # Create socket and listen for client connections
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        print(f'Server listening on {HOST}:{PORT}')
        
        while True:
            conn, addr = server_socket.accept()
            print(f'Connection from {addr}')
            handle_client_connection(conn)

if __name__ == "__main__":
    start_server()