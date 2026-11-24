import socket
import ssl
import tkinter
import customtkinter

from tkinterweb import HtmlFrame
from urllib.parse import urlparse, urljoin


# CustomTkinter
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

app.geometry(f"{screen_width // 2}x{screen_height // 2}")
app.title("My Browser")


# HTTP Client
def fetch_url(url):
    """
    Fetch a web page using a raw socket.
    Returns the HTML body.
    """

    parsed = urlparse(url)

    scheme = parsed.scheme
    host = parsed.hostname
    port = parsed.port

    if not host:
        raise ValueError("Invalid URL")

    # Default ports
    if port is None:
        port = 443 if scheme == "https" else 80

    # Path
    path = parsed.path or "/"

    if parsed.query:
        path += "?" + parsed.query

    # Create TCP socket
    sock = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    try:
        print(f"Connecting to {host}:{port}...")

        # HTTPS
        if scheme == "https":

            context = ssl.create_default_context()

            sock = context.wrap_socket(
                sock,
                server_hostname=host
            )

        # TCP connection
        sock.connect((host, port))

        print("Connected!")

        #HTTP Request
        request = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            f"User-Agent: MyBrowser/1.0\r\n"
            f"Accept: text/html\r\n"
            f"Connection: close\r\n"
            f"\r\n"
        )

        print("\n--- REQUEST ---")
        print(request)

        sock.sendall(request.encode("utf-8"))

        # Receive Response
        response = b""

        while True:

            data = sock.recv(4096)

            if not data:
                break

            response += data

        print("\n--- RESPONSE SIZE ---")
        print(f"{len(response)} bytes")

        # Convert bytes -> string
        response = response.decode(
            "utf-8",
            errors="replace"
        )

        # Separate headers/body
        if "\r\n\r\n" not in response:
            raise ValueError("Invalid HTTP response")

        headers, body = response.split(
            "\r\n\r\n",
            1
        )

        print("\n--- RESPONSE HEADERS ---")
        print(headers)

        return body

    finally:
        sock.close()

        print("\nConnection closed.")

# Browser navigation
def search():
    url = url_input.get().strip()

    if not url:
        return

    # Add scheme if user didn't type it
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:

        print("\n==============================")
        print(f"Loading: {url}")
        print("==============================")

        html = fetch_url(url)

        # Render HTML
        browser.load_html(html)

        # Save current URL
        current_url.set(url)

    except Exception as error:

        print(f"Error: {error}")

        browser.load_html(
            f"""
            <html>
                <body>
                    <h2>Unable to load page</h2>
                    <p>{error}</p>
                </body>
            </html>
            """
        )


# URL input
url_input = customtkinter.CTkEntry(
    app,
    placeholder_text="Enter URL...",
    width=600,
    height=45,
    font=("Arial", 16)
)

url_input.pack(
    pady=20
)

# Search button
search_button = customtkinter.CTkButton(
    app,
    text="Go",
    command=search,
    width=120,
    height=45,
    font=("Arial", 16)
)

search_button.pack(
    pady=(0, 10)
)


# Current URL
current_url = tkinter.StringVar()

url_label = customtkinter.CTkLabel(
    app,
    textvariable=current_url
)

url_label.pack()


# Browser
browser = HtmlFrame(
    app,
    messages_enabled=True
)

browser.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=20
)


# Enter key
app.bind(
    "<Return>",
    lambda event: search()
)

# Start application
app.mainloop()