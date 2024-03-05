from flask import Flask, render_template, jsonify, request, redirect, url_for
from tic_tac_toe import TicTacToe, HumanPlayer, SmartComputerPlayer,computer_winning_prob,matched_cells

app = Flask(__name__)
game = TicTacToe()
human_player = HumanPlayer('X')
ai_player = SmartComputerPlayer('O')

@app.route('/home')
def hom():
    return "vamsi krishna"


@app.route('/main')
def index():
    return render_template('index.html', board=game.board)
    

@app.route('/ai_move',methods=['GET'])
def ai_move():
    ai_square = ai_player.get_move(game)
    game.make_move(ai_square, ai_player.letter)
    total_games = computer_winning_prob[1] + computer_winning_prob[-1] + computer_winning_prob[0]
    winning_percentage = computer_winning_prob[1] * 100 / total_games if total_games != 0 else 0
    losing_percentage = computer_winning_prob[-1] * 100 / total_games if total_games != 0 else 0
    tie_percentage = computer_winning_prob[0] * 100 / total_games if total_games != 0 else 0
    return jsonify({'message': 'Move Successful', 'board': game.board, 'winning': winning_percentage, 'loss': losing_percentage, 'tie':tie_percentage}), 200

@app.route('/make_move/<int:square>', methods=['GET'])
def make_move(square):
    if game.make_move(square, human_player.letter):
        if game.current_winner:
            return jsonify({'message': 'Game Over','board': game.board, 'winner': game.current_winner,'winning': 0, 'loss': 0, 'tie': 0}), 200
       
        if game.empty_squares():
            ai_square = ai_player.get_move(game)
            game.make_move(ai_square, ai_player.letter)
            if game.current_winner:
                winning_cells=game.wincells(ai_square, ai_player.letter)
                return jsonify({'message': 'Game Over','board': game.board, 'winner': game.current_winner,'winning': 0, 'loss': 0, 'tie': 0,'cells':winning_cells}), 200
            if not game.empty_squares():
                return jsonify({'message': 'Draw','board': game.board, 'winner': game.current_winner,'winning': 0, 'loss': 0, 'tie': 0}), 200             
        else:
            return jsonify({'message': 'Draw','board': game.board, 'winner': game.current_winner,'winning': 0, 'loss': 0, 'tie': 0}), 200
        
        total_games = computer_winning_prob[1] + computer_winning_prob[-1] + computer_winning_prob[0]
        winning_percentage = computer_winning_prob[1] * 100 / total_games if total_games != 0 else 0
        losing_percentage = computer_winning_prob[-1] * 100 / total_games if total_games != 0 else 0
        tie_percentage = computer_winning_prob[0] * 100 / total_games if total_games != 0 else 0
        return jsonify({'message': 'Move Successful', 'board': game.board, 'winning': winning_percentage, 'loss': losing_percentage, 'tie':tie_percentage}), 200
    return jsonify({'message': 'Invalid move'}), 400

@app.route('/restart', methods=['GET'])
def restart():
    global game
    game = TicTacToe()
    return jsonify({'message': 'Game restarted'}), 200


if __name__ == '__main__':
    app.run(debug=True)
