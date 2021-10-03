from flask import Flask, jsonify, render_template, request
import data_debris

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/data-space-debris/<param>/<time>', methods=['GET'])
def data_space_debris(param, time):
    """
    Retrieve all satellite data (coordinates and IDs) in due course

    :param param: the satellite category (from 0 to 6)
    :type param: string

    :param time: the time stamp on the time bar on the website (if 0 then default state -> real time; if not 0 then there has been a time change)
    :type time: string

    :return: the dictionary containing all of coordinates and IDs
    :rtype: json
    """

    if request.method == 'GET':
        dictionnaire = data_debris.data_in_dict(param, time)
        return jsonify(dictionnaire)


@app.route('/get-new-time/<time>', methods=['GET'])
def get_new_time(time):
    """
    Retrieve the date with the additional time

    :param time: additional time
    :type time: str

    :return: the date with the additional time
    :rtype: json
    """

    if request.method == 'GET':
        str_new_time = data_debris.get_new_time(time)
        return jsonify(str_new_time)


if __name__ == '__main__':
    app.run()