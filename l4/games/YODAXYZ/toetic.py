class Tic(object):
    board = [i for i in range(1, 10)]

    def draw_board(self):
        """ Draw  field"""
        print('-------------')
        for i in range(3):
            print('| {0} | {1} | {2} |'.format(self.board[0+i*3], self.board[1+i*3], self.board[2+i*3]))
            print('-------------')

    def take_input(self, player_token):
        """ Players courserses """
        valid = False
        while not valid:
            player_ans = input("Where to put " + player_token + "\n")

            try:
                player_ans = int(player_ans)
            except:
                print("Error are you sure that you entered a number ?")
                continue
            if player_ans >= 1 and player_ans <= 9:
                if str(self.board[player_ans-1]) not in 'XO':
                    self.board[player_ans-1] = player_token
                    valid = True
                else:
                    print("This cell has value")
            else:
                print("Incorrect input. Enter a number between 1 and 9 to walk")

    def check_win(self):
        """ Check win """
        win_position = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        for each in win_position:
            if self.board[each[0]] == self.board[each[1]] == self.board[each[2]]:
                return self.board[each[0]]
        return False

    def run(self):
        counter = 0
        win = False
        while not win:
            self.draw_board()
            if counter % 2 == 0:
                self.take_input('X')
            else:
                self.take_input('O')
            counter += 1
            if counter > 4:
                tmp = self.check_win()
                if tmp:
                    print(tmp,  " Win")
                    win = True
                    break
            if counter == 9:
                print("Draw!")
                break
        self.draw_board()


def main():
    tic_tac_toi = Tic()
    tic_tac_toi.run()
    

if __name__ == '__main__':
    main()

