from playsound import playsound


class AudioManager:
    def __init__(self):
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
        self.kennedy_wins = True
        self.loser = True
        self.play_tictactoe = True
        self.praise_moloch = True
        self.ready = True
        self.rematch = True
        self.robot_overlord_kennedy = True
        self.terrible_move = True
        self.tie = True
        self.ttt_explain_ending = True
        self.ttt_explain_objective = True
        self.ttt_explain_play = True
        self.ttt_explain_setup = True
        self.ttt_explain_tokens_setup = True
        self.ttt_explain_winning = True
        self.umm = True
        self.well_played = True

    def play_game_over(self):
        if self.game_over:
            playsound("SoundFiles/game_over.wav", block=True)

    def play_gg(self):
        if self.gg:
            playsound("SoundFiles/gg.wav", block=True)

    def play_good_move(self):
        if self.good_move:
            playsound("SoundFiles/good_move.wav", block=True)

    def play_hello_i_am_handy(self):
        if self.hello_i_am_handy:
            playsound("SoundFiles/hello_i_am_handy.wav", block=True)

    def play_hmm(self):
        if self.hmm:
            playsound("SoundFiles/hmm.wav", block=True)

    def play_hmm2(self):
        if self.hmm2:
            playsound("SoundFiles/hmm2.wav", block=True)

    def play_instructions_question(self):
        if self.instructions_question:
            if self.instructions_counter < 1:
                playsound("SoundFiles/instructions_question.wav", block=False)
            else:
                playsound("SoundFiles/instructions_question_again.wav", block=False)

    def play_its_your_move(self):
        if self.its_your_move:
            playsound("SoundFiles/its_your_move.wav", block=True)

    def play_kennedy_loses(self):
        if self.kennedy_loses:
            playsound("SoundFiles/kennedy_loses.wav", block=True)

    def play_kennedy_wins(self):
        if self.kennedy_wins:
            playsound("SoundFiles/kennedy_wins.wav", block=True)

    def play_loser(self):
        if self.loser:
            playsound("SoundFiles/loser.wav", block=True)

    def play_play_tictactoe(self):
        if self.play_tictactoe:
            playsound("SoundFiles/play_tictactoe.wav", block=True)

    def play_praise_moloch(self):
        if self.praise_moloch:
            playsound("SoundFiles/praise_moloch.wav", block=True)

    def play_ready(self):
        if self.ready:
            playsound("SoundFiles/ready.wav", block=True)

    def play_rematch(self):
        if self.rematch:
            playsound("SoundFiles/rematch.wav", block=True)

    def play_robot_overlord_kennedy(self):
        if self.robot_overlord_kennedy:
            playsound("SoundFiles/robot_overlord_kennedy.wav", block=True)

    def play_terrible_move(self):
        if self.terrible_move:
            playsound("SoundFiles/terrible_move.wav", block=True)

    def play_tie(self):
        if self.tie:
            playsound("SoundFiles/tie.wav", block=True)

    def play_ttt_explain_ending(self):
        if self.ttt_explain_ending:
            playsound("SoundFiles/ttt_explain_ending_condition.wav", block=True)

    def play_ttt_explain_objective(self):
        if self.ttt_explain_objective:
            playsound("SoundFiles/ttt_explain_objective.wav", block=True)

    def play_ttt_explain_play(self):
        if self.ttt_explain_play:
            playsound("SoundFiles/ttt_explain_play.wav", block=True)

    def play_ttt_explain_setup(self):
        if self.ttt_explain_setup:
            playsound("SoundFiles/ttt_explain_setup.wav", block=True)
            self.instructions_counter += 1

    def play_ttt_explain_tokens_setup(self):
        if self.ttt_explain_tokens_setup:
            playsound("SoundFiles/ttt_explain_tokens_setup.wav", block=True)

    def play_ttt_explain_winning(self):
        if self.ttt_explain_winning:
            playsound("SoundFiles/ttt_explain_winning.wav", block=True)

    def play_umm(self):
        if self.umm:
            playsound("SoundFiles/umm.wav", block=True)

    def play_well_played(self):
        if self.well_played:
            playsound("SoundFiles/well_played.wav", block=True)
