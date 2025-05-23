from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from views.user_requests import create_user, login_user, get_all_users, get_single_user, delete_user, update_user


from views.post_requests import get_single_post, get_all_posts, create_post, delete_post, update_post


from views.subscription_requests import get_all_subscriptions, create_subscription, delete_subscription
from views.category_requests import get_all_categories, create_category, delete_category

from views import get_comments_by_post, create_comments, delete_comments, update_comments


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        self._set_headers(200)

        response = {}

        parsed = self.parse_url()

        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "users":
                if id is not None:
                    response = get_single_user(id)

                else:
                    response = get_all_users()

            if resource == "categories":
                if id is not None:
                    response = get_single_category(id)
                else:
                    response = get_all_categories()

            if resource == "posts":
                if id is not None:
                    response = get_single_post(id)

                else:
                    response = get_all_posts()

            if resource == "subscriptions":
                response = get_all_subscriptions()

        else:
            (resource, key, value) = parsed

            if key == 'post_id' and resource == "comments":
                response = get_comments_by_post(value)
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)
        if resource == 'users':
            response = create_user(post_body)
        if resource == 'subscriptions':
            response = create_subscription(post_body)
        if resource == 'comments':
            response = create_comments(post_body)

        if resource == 'posts':
            response = create_post(post_body)

        if resource == 'categories':
            response = create_category(post_body)


        self.wfile.write(response.encode())

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url()

        success = False

        if resource == "users":
            success = update_user(id, post_body)
            
        if resource == "posts":
            success = update_post(id, post_body)
            
        if resource == "comments":
            success = update_comments(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        self._set_headers(204)

        (resource, id) = self.parse_url()

        if resource == "users":
            delete_user(id)
        if resource == "subscriptions":
            delete_subscription(id)
        if resource == "comments":
            delete_comments(id)
        if resource == "categories":
            delete_category(id)
        self.wfile.write("".encode())
        
        if resource == "posts":
            delete_post(id)
        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
