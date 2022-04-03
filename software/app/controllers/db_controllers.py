import sqlite3
import pickle


# Класс для работы с БД
class ParserDB:
    def __init__(self, database_name):  # При инициализации передаем название файла БД
        self.connection = sqlite3.connect(database_name)
        self.cursor = self.connection.cursor()

    def create_new_db(self):
        with self.connection:
            self.cursor.execute('CREATE TABLE games (id integer primary key,\
             positions blob, moves blob, begindate blob, winner blob)')

    # Сохраняем игру в БД
    def save_game(self, chessgame):
        positions, moves, begindate, winner = chessgame.get_all_data()
        pklpositions = pickle.dumps(positions)
        pklmoves = pickle.dumps(moves)
        pklbegindate = pickle.dumps(begindate)
        pklwinner = pickle.dumps(winner)
        with self.connection:
            self.cursor.execute('INSERT INTO games (positions, moves, begindate, winner) VALUES (?, ?, ?, ?)',
                                (pklpositions, pklmoves, pklbegindate, pklwinner))

    def delete_game(self, id):
        with self.connection:
            self.cursor.execute('DELETE FROM games WHERE id=?', (id,))


# Пример использования бд
# from app.models import ChessGame, GamePlayer
# from datetime import date
# pdb = ParserDB("games.db")
# pdb.create_new_db()
# white_player = GamePlayer('Billy', 'Jones', '1990')
# black_player = GamePlayer('Jonny', 'Jones', '1990')
# chess_game = ChessGame.create_game_with_zero_moves(date.today(), ChessGame.GameOutcome.white, white_player, black_player)
# pdb.save_game(chess_game)
# pdb.delete_game(1)
