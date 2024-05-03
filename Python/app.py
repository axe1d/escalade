from flask import Flask, request, jsonify, send_from_directory
import csv
from uuid import uuid4

app = Flask(__name__, static_folder='escalade/build', static_url_path='/')

# @app.route('/')
# def serve():
#     return send_from_directory(app.static_folder, 'index.html')

def find_user_in_csv(first_name, last_name):
    with open('access_codes.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['first_name'] == first_name and row['last_name'] == last_name:
                return row['access_code']
    return None


def remove_first_line(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()  # Read all lines into a list
    # Store the first line if needed
    first_line = lines[0] if lines else None
    # Write back all lines except the first one
    with open(filename, 'w') as file:
        file.writelines(lines[1:])
    return first_line


@app.route('/api/generate-access-code', methods=['POST'])
def generate_access_code():
    data = request.json
    first_name = data.get('firstName')
    last_name = data.get('lastName')
    existing_code = find_user_in_csv(first_name, last_name)

    if existing_code:
        return jsonify({'accessCode': existing_code})

    # Create a new access code
    new_access_code = str(remove_first_line('codes_available.csv'))
    with open('access_codes.csv', mode='a', newline='') as csvfile:
        fieldnames = ['first_name', 'last_name', 'access_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if csvfile.tell() == 0:
            writer.writeheader()
        writer.writerow({'first_name': first_name, 'last_name': last_name, 'access_code': new_access_code})

    return jsonify({'accessCode': new_access_code})


if __name__ == '__main__':
    app.run(use_reloader=True, port=5000, threaded=True)
