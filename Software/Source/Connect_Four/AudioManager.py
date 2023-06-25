from playsound import playsound


class AudioManager:
    def __init__(self):
        self.connect_four_explain_ending = True
        self.connect_four_explain_objective = True
        self.connect_four_explain_play = True
        self.connect_four_explain_setup = True
        self.connect_four_explain_tokens_setup = True
        self.connect_four_explain_winning = True
        self.game_over = True
        self.gg = True
        self.good_move = True
        self.hello_i_am_handy = True
        self.hmm = True
        self.hmm2 = True
        self.instructions_question = True
        self.instructions_counter = 0
        self.its_your_move = True
        self.kennedy_loses = True
        self.kennedy_plays_red = True
        self.kennedy_plays_yellow = True
        self.kennedy_wins = True
        self.loser = True
        self.play_connect_four = True
        self.praise_moloch = True
        self.ready = True
        self.rematch = True
        self.robot_overlord_kennedy = True
        self.terrible_move = True
        self.tie = True
        self.umm = True
        self.well_played = True
        self.fraction_for_gg = 0.7
        self.gg_occurred = False
        self.umm_threshold = -8

    def play_connect_four_explain_ending(self):
        if self.connect_four_explain_ending:
            playsound("SF/01.wav", block=True)

    def play_connect_four_explain_objective(self):
        if self.connect_four_explain_objective:
            playsound("SF/02.wav", block=True)

    def play_connect_four_explain_play(self):
        if self.connect_four_explain_play:
            playsound("SF/03.wav", block=True)

    def play_connect_four_explain_setup(self):
        if self.connect_four_explain_setup:
            playsound("SF/04.wav", block=True)
            self.instructions_counter += 1

    def play_connect_four_explain_tokens_setup(self):
        if self.connect_four_explain_tokens_setup:
            playsound("SF/05.wav", block=True)

    def play_connect_four_explain_winning(self):
        if self.connect_four_explain_winning:
            playsound("SF/06.wav", block=True)

    def play_game_over(self):
        if self.game_over:
            playsound("SF/07.wav", block=True)

    def play_gg(self):
        if self.gg:
            playsound("SF/08.wav", block=True)
            self.gg_occurred = True

    def play_good_move(self):
        if self.good_move:
            playsound("SF/09.wav", block=True)

    def play_hello_i_am_handy(self):
        if self.hello_i_am_handy:
            playsound("SF/10.wav", block=True)

    def play_hmm(self):
        if self.hmm:
            playsound("SF/11.wav", block=False)

    def play_hmm2(self):
        if self.hmm2:
            playsound("SF/12.wav", block=False)

    def play_instructions_question(self):
        if self.instructions_question:
            if self.instructions_counter < 1:
                playsound("SF/13.wav", block=False)
            else:
                playsound("SF/14.wav", block=False)

    def play_its_your_move(self):
        if self.its_your_move:
            playsound("SF/15.wav", block=False)

    def play_kennedy_loses(self):
        if self.kennedy_loses:
            playsound("SF/16.wav", block=True)

    def play_kennedy_plays_red(self):
        if self.kennedy_plays_red:
            playsound("SF/17.wav", block=True)

    def play_kennedy_plays_yellow(self):
        if self.kennedy_plays_yellow:
            playsound("SF/18.wav", block=True)

    def play_kennedy_wins(self):
        if self.kennedy_wins:
            playsound("SF/19.wav", block=True)

    def play_loser(self):
        if self.loser:
            playsound("SF/20.wav", block=True)

    def play_play_connect_four(self):
        if self.play_connect_four:
            playsound("SF/21.wav", block=True)

    def play_praise_moloch(self):
        if self.praise_moloch:
            playsound("SF/22.wav", block=True)

    def play_ready(self):
        if self.ready:
            playsound("SF/23.wav", block=True)

    def play_rematch(self):
        if self.rematch:
            playsound("SF/24.wav", block=False)

    def play_robot_overlord_kennedy(self):
        if self.robot_overlord_kennedy:
            playsound("SF/25.wav", block=True)

    def play_terrible_move(self):
        if self.terrible_move:
            playsound("SF/26.wav", block=True)

    def play_tie(self):
        if self.tie:
            playsound("SF/27.wav", block=True)

    def play_umm(self):
        if self.umm:
            playsound("SF/28.wav", block=True)

    def play_well_played(self):
        if self.well_played:
            playsound("SF/29.wav", block=True)
