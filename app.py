from flask import Flask, render_template, request
import matplotlib
matplotlib.use('Agg')   # Needed for servers without GUI
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    graph_url = None

    if request.method == 'POST':
        func_str = request.form['function']

        # Create x range
        x = np.linspace(-10, 10, 400)

        # Safely evaluate function
        try:
            y = eval(func_str, {"__builtins__": {}}, {"x": x, "np": np})

            # Plot the function
            plt.figure()
            plt.plot(x, y)
            plt.xlabel("x")
            plt.ylabel("y")
            plt.title(f"y = {func_str}")

            # Save image to a string buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png')
            buffer.seek(0)
            img_png = buffer.getvalue()
            buffer.close()

            graph_url = base64.b64encode(img_png).decode('ascii')

        except Exception as e:
            graph_url = None

    return render_template('index.html', graph_url=graph_url)

if __name__ == "__main__":
    app.run(debug=True)
