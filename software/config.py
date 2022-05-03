import assets.resources_rc
from logging import DEBUG


class Config(object):
    log_file = 'chess.log'
    log_level = DEBUG
    db_uri = 'sqlite:///chess.sqlite'
    main_window_ui_path = 'app/views/main_window.ui'
    game_player_resolve_step_select_opt_dialog = 'game_player_resolve_step_select_opt_dialog.ui'
    game_player_resolve_step_choose_player_opt_dialog = 'game_player_resolve_step_choose_player_opt_dialog.ui'
    game_player_resolve_step_create_player_opt_dialog = 'game_player_resolve_step_create_player_opt_dialog.ui'

    chessboard_size = 500
    chessboard_x = 0
    chessboard_y = 0
    chessboard_fig_size = chessboard_size / 8
    chessboard_default_white_cell_color = '#F0D9B5'
    chessboard_default_black_cell_color = '#B58863'
    chessboard_highlight_white_cell_color = '#F7EC74'
    chessboard_highlight_black_cell_color = '#DAC34B'
    chessboard_view_background_color = '#4b544d'
    chessboard_zoom_in_factor = 1.25

    play_tool_button_pixmap_path = ':/icons/img/icons/play.png'
    pause_tool_button_pixmap_path = ':/icons/img/icons/pause.png'

    bb_path = ':/pieces/img/pieces/bb.png'
    bk_path = ':/pieces/img/pieces/bk.png'
    bn_path = ':/pieces/img/pieces/bn.png'
    bp_path = ':/pieces/img/pieces/bp.png'
    bq_path = ':/pieces/img/pieces/bq.png'
    br_path = ':/pieces/img/pieces/br.png'
    wb_path = ':/pieces/img/pieces/wb.png'
    wk_path = ':/pieces/img/pieces/wk.png'
    wn_path = ':/pieces/img/pieces/wn.png'
    wp_path = ':/pieces/img/pieces/wp.png'
    wq_path = ':/pieces/img/pieces/wq.png'
    wr_path = ':/pieces/img/pieces/wr.png'

    wait_gif_path = ':/icons/img/icons/wait.gif'
    checked_path = ':/icons/img/icons/checked.png'