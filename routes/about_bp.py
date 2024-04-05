from flask import Blueprint, render_template

users = [
    {
        "id": "1",
        "name": "Gemma",
        "pic": "https://th.bing.com/th/id/OIP.rS1lWWgFD0gV-nbP2XxdVgAAAA?w=416&h=315&rs=1&pid=ImgDetMain",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Lilitha",
        "pic": "https://th.bing.com/th/id/OIP.ZP-E8ZFH11wb1XSm0dn-5wHaJQ?rs=1&pid=ImgDetMain",
        "pro": False,
    },
    {
        "id": "3",
        "name": "Caleb",
        "pic": "https://cdn.lifehack.org/wp-content/uploads/2015/02/what-makes-people-happy.jpeg",
        "pro": True,
    },
]


about_bp = Blueprint("about", __name__)


@about_bp.route("/")
def about_page():
    return render_template("about.html", users=users)


@about_bp.route("/<id>")
def about_user(id):
    filtered_user = [user for user in users if user["id"] == id]
    return render_template("about.html", users=filtered_user)
