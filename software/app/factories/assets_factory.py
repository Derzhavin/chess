from PyQt5.QtGui import QPixmap, QIcon
from singleton_decorator import singleton
from app.models import ChessFigure


@singleton
class AssetsFactory(object):

    def __init__(self, config=None):
        super().__init__()
        
        if config is None:
            return

        self.play_tool_button_pixmap = QIcon(QPixmap(config.play_tool_button_pixmap_path))
        self.pause_tool_button_pixmap = QIcon(QPixmap(config.pause_tool_button_pixmap_path))
        self.figure_pixmap = {
            ChessFigure.bb: QPixmap(config.bb_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.bk: QPixmap(config.bk_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.bn: QPixmap(config.bn_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.bp: QPixmap(config.bp_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.bq: QPixmap(config.bq_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.br: QPixmap(config.br_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wb: QPixmap(config.wb_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wk: QPixmap(config.wk_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wn: QPixmap(config.wn_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wp: QPixmap(config.wp_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wq: QPixmap(config.wq_path).scaledToWidth(config.chessboard_fig_size),
            ChessFigure.wr: QPixmap(config.wr_path).scaledToWidth(config.chessboard_fig_size)
        }

        self.checked_pixmap = QPixmap(config.checked_path).scaledToWidth(64)