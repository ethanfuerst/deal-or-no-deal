import random
import sys


CASE_VALS = [
    0.01, 1, 5, 10, 
    25, 50, 75, 100, 
    200, 300, 400, 500, 
    750, 1000, 5000, 10000, 
    25000, 50000, 75000, 100000, 
    200000, 300000, 400000, 500000, 
    750000, 1000000]

class Case():
    def __init__(self, value, num):
        self.value = value
        self.available = True
        self.num = num

    def __str__(self):
        return '[' + str(self.num) + ']'

class DealOrNoDeal():

    def __init__(self, case_vals=CASE_VALS):
        # values left to win
        self.case_vals = sorted(case_vals)
        self.vals_left = case_vals

        # all cases on the board
        random.shuffle(case_vals)
        self.cases = [Case(value, num) for num, value in enumerate(case_vals, 1)]

        # case chosen by contestant at the beginning
        self.__choice_case = None

        # must add up to len(case_vals) - 2
        self.rounds = [5, 5, 5, 5, 3, 1]

        self.offers = []

        self.playing = True

    def print_cases(self):
        '''prints current board'''

        # figure out how to dynamically print cases with any length of case_vals
        print('  '.join([str(i) if i.available else '    ' for i in self.cases[:7]]))
        print('   ' + '  '.join([str(i) if i.available else '    ' for i in self.cases[7:13]]))
        print('  '.join([str(i) if i.available else '    ' for i in self.cases[13:20]]))
        print('   ' + '  '.join([str(i) if i.available else '    ' for i in self.cases[20:]]))
        
        if self.__choice_case:
            print('\n\t\t\tYour case: ' + str(self.__choice_case) + '\n')

        num_rows = len(self.case_vals) // 2
        max_len = len(str(max(self.case_vals[:len(self.case_vals) // 2])))

        for i, j in zip(self.case_vals[:len(self.case_vals) // 2], self.case_vals[len(self.case_vals) // 2:]):

            if i not in self.vals_left:
                i = '\u0336'.join(str(i)) + '\u0336'
        
            if j not in self.vals_left:
                j = '\u0336'.join(str(j)) + '\u0336'
            
            print('\t' + str(i) + ' ' * (max_len - len(str(i))) +'\t\t' + str(j))

        return

    def get_dealer_offer(self):
        '''returns dealer offer at game state'''

        return round((sum(self.vals_left) / len(self.vals_left)) * (random.randrange(75, 86) / 100), 2)

    def get_case_choice(self):
        '''returns case index given case number'''

        num = input('Choose a case number: ')
        try:
            num = int(num)
            if num not in [i.num for i in self.cases if i.available]:
                print("That case isn't available. I'll choose one at random for you")
                num = random.choice([i.num for i in self.cases if i.available])
        except ValueError:
            print("I don't recognize that number! I'll choose a random case for you")
            num = random.choice([i.num for i in self.cases if i.available])
        
        return num - 1

    def get_deal_choice(self):
        '''gets dealer offer and if player accepted the offer'''

        offer = self.get_dealer_offer()
        self.offers.append(offer)

        print(f'The dealers offer is: ${offer}')
        deal = input('Deal (Y) or No Deal (N)? ')

        if deal.upper() == 'Y':
            return True

        return False

    def reveal_cases(self, num):
        '''reveals given number of cases'''

        for i in range(num):

            choice = self.get_case_choice()
            print(str(self.cases[choice]) + ' - $' + str(self.cases[choice].value))

            self.cases[choice].available = False
            self.vals_left.remove(self.cases[choice].value)

        return

    def get_final_choice(self):
        '''facilitates final choice at end of game'''

        self.print_cases()
        decision = input('Do you want your original case (Y) or the last case left (N)? ')

        if decision == 'Y':
            return self.__choice_case

        return [i for i in self.cases if i.available][0]

    def game_end(self, deal):
        '''facilitates end of game'''

        if deal:
            print(f'You left with ${self.offers[-1]}')
        else:
            # final case left - offer is made and then you choose the case
            final_choice = self.get_final_choice()
            
            print(f'Your final winnings are: ${str(final_choice.value)}')
            print('Offers you turned down: $' + ', $'.join(map(str, self.offers)))
            # was final score higher than offers? if so, how many?
        
        return

    def play(self):
        print('Welcome to Deal or No Deal!')
        while self.playing:
            self.print_cases()
            
            # choose a case
            print('Choose a case to begin.')
            choice = self.get_case_choice()
            self.__choice_case = self.cases[choice]
            # make case unavailable but keep value in the vals_left
            self.cases[choice].available = False
            
            print("Let's get started!")
            self.print_cases()

            for cases_to_open in self.rounds:
                
                print(f'open {cases_to_open} cases')
                # open x number of cases
                self.reveal_cases(cases_to_open)
                self.print_cases()

                deal = self.get_deal_choice()
                if deal:
                    print('You accepted the deal!')
                    self.playing = False
                    break
                else:
                    print(f'Just turned down ${self.offers[-1]}')
                    self.print_cases()

            self.game_end(deal)
            print('Game over!')
            
            self.playing = False

        return

if __name__ == '__main__':
    DealOrNoDeal().play()
