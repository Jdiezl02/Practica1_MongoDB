from flask import Flask, jsonify, request
from neo4j import GraphDatabase
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "12345678"))

@app.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    name = data.get("name")
    if not username or not name:
        return jsonify({"error": "username y name son obligatorios"}), 400
    with driver.session() as session:
        session.run("""
            MERGE (u:User {username: $username})
            SET u.name = $name
        """, username=username, name=name)
    return jsonify({"status": "ok", "message": f"Usuario {username} creado."})

@app.route("/posts", methods=["POST"])
def create_post():
    data = request.get_json()
    username = data.get("username")
    contennt = data.get("contennt")
    if not username or not contennt:
        return jsonify({"error": "username y content son obligatorios"}), 400
    with driver.session() as session:
        session.run("""
            MATCH (u:User {username: $username})
            CREATE (u)-[:POSTED]->(p:Post {contennt: $contennt, timestamp: datetime()})
        """, username=username, contennt=contennt)
    return jsonify({"status": "ok", "message": f"Post creado para {username}"})

@app.route("/users/<username>/posts", methods=["GET"])
def get_user_posts(username):
    with driver.session() as session:
        result = session.run("""
            MATCH (u:User {username: $username})-[:POSTED]->(p:Post)
            RETURN p.contennt AS contennt, p.timestamp AS fecha
            ORDER BY p.created_at DESC
        """, username=username)
        posts = [record.data() for record in result]
    return jsonify(posts)

@app.route("/follow", methods=["POST"])
def follow_user():
    data = request.get_json()
    user_from = data.get("from")
    user_to = data.get("to")
    if not user_from or not user_to:
        return jsonify({"error": "from y to son obligatorios"}), 400
    with driver.session() as session:
        session.run("""
            MATCH (a:User {username: $user_from}), (b:User {username: $user_to})
            MERGE (a)-[:FOLLOWS]->(b)
        """, user_from=user_from, user_to=user_to)
    return jsonify({"status": "ok", "message": f"{user_from} ahora sigue a {user_to}."})

@app.route("/mutual_follows", methods=["GET"])
def mutual_follows():
    with driver.session() as session:
        result = session.run("""
            MATCH (a:User)-[:FOLLOWS]->(b:User),
                  (b)-[:FOLLOWS]->(a)
            WHERE a.username < b.username
            RETURN a.username AS user1, b.username AS user2
            ORDER BY user1, user2
        """)
        mutuals = [record.data() for record in result]
    return jsonify(mutuals)

@app.route("/users", methods=["GET"])
def get_users():
    with driver.session() as session:
        result = session.run("MATCH (u:User) RETURN u.username AS username, u.name AS name")
        users = [record.data() for record in result]
    return jsonify(users)

@app.route("/posts", methods=["GET"])
def get_psot():
    with driver.session() as session:
        result = session.run("MATCH (p:Post) RETURN p.contennt AS content, p.timestamp AS fecha")
        users = [record.data() for record in result]
    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)
