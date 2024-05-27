import random


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        # suits = ["spades", "club", "hearts", "diamonds"]
        suits = ["♠️", "♣️", "♥️", "♦️"]
        ranks = [
            {"rank": "A", "value": 11},
            {"rank": "2", "value": 2},
            {"rank": "3", "value": 3},
            {"rank": "4", "value": 4},
            {"rank": "5", "value": 5},
            {"rank": "6", "value": 6},
            {"rank": "7", "value": 7},
            {"rank": "8", "value": 8},
            {"rank": "9", "value": 9},
            {"rank": "10", "value": 10},
            {"rank": "J", "value": 10},
            {"rank": "Q", "value": 10},
            {"rank": "K", "value": 10},
        ]

        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):  # ? မွေတာ
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):  # ? ကတ်ထပ်ဆွဲတာ
        cards_dealt = []
        for x in range(number):
            if len(self.cards) > 0:
                card = self.cards.pop()
                cards_dealt.append(card)
        return cards_dealt


class Hand:
    def __init__(self, dealer=False):
        self.cards = []
        self.value = 0
        self.dealer = dealer

    def add_card(self, card_list):
        self.cards.extend(card_list)

    def calculate_value(self):
        self.value = 0
        has_ace = False

        for card in self.cards:
            card_value = int(card.rank['value'])
            self.value += card_value
            if card.rank['rank'] == 'A':
                has_ace = True

        if has_ace and self.value > 21:  # ? if A နှစ်ကဒ် ဆိုရင် ၁၁ မ ယူဘဲ ၁ယူတာ
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        print(f'''{"Dealer's" if self.dealer else "Your"} hand:''')
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer \
                    and not show_all_dealer_cards and not self.is_blackjack():  # ! dealer ရဲ့ (ပထမဆုံးကဒ် ကို မပြတာ)
                print('hidden')
            else:
                print(card)  # ! show Card

        if not self.dealer:  # ? Player ပဲ Value ကို ပြမယ်
            print("Value : ", self.get_value())
        print()


class Game:
    def play(self):
        game_number = 0
        games_to_play = 0
        self.player_wins = 0
        self.dealer_wins = 0

        while games_to_play <= 0:
            try:
                games_to_play = int(input('How many games do you want to play? '))
            except:
                print("You must enter a number.")

        while game_number < games_to_play:
            game_number += 1

            deck = Deck()
            deck.shuffle()

            player_hand = Hand()
            dealer_hand = Hand(dealer=True)

            for i in range(2):
                player_hand.add_card(deck.deal(1))
                dealer_hand.add_card(deck.deal(1))

            print()
            print("*" * 30)
            print(f"Game {game_number} of {games_to_play}")
            print("*" * 30)

            player_hand.display()
            dealer_hand.display()

            # ? 21 ထပ်များသွားပြီလားရယ် Blackjack result မထွက်သေးရင် ထပ်ဆွဲဖို့အတွက် ဆင်းမယ်
            if self.check_winner(player_hand,
                                 dealer_hand):
                continue

                # ? player ထပ်ဆွဲမဆွဲ အတွက်
            choice = ""
            while player_hand.get_value() < 21 and choice not in ['s', 'stand']:  # ? 21 ထပ်ငယ်နေသေးတယ် ဆိုရင်
                choice = input("Please choose 'Hit' or 'Stand' : ").lower()
                print()
                while choice not in ["h", "s", "hit", "stand"]:
                    choice = input("Please enter 'Hit' or 'Stand' (or H/S) ").lower()
                    print()
                if choice in ["hit", "h"]:
                    player_hand.add_card(deck.deal(1))
                    player_hand.display()

            if self.check_winner(player_hand,
                                 dealer_hand):
                # ? 21 ထပ်များသွားပြီလားရယ် Blackjack result မထွက်သေးရင် ထပ်ဆွဲဖို့အတွက် ဆင်းမယ်
                continue

            player_hand_value = player_hand.get_value()
            dealer_hand_value = dealer_hand.get_value()
            limit_dealer_card_value = 17

            # ? dealer limit ထပ်နည်းနေသေးတယ်ဆိုရင် ထပ်ဆွဲခိုင်းထားတာ
            while dealer_hand_value < limit_dealer_card_value:
                dealer_hand.add_card(deck.deal(1))
                dealer_hand_value = dealer_hand.get_value()

            dealer_hand.display(show_all_dealer_cards=True)  # ? dealer limit ထပ်များသွားတာနဲ့ show ခိုင်းတာ

            # ? 21 ထပ်များသွားပြီလားရယ် Blackjack result မထွက်သေးရင် ထပ်ဆွဲဖို့အတွက် ဆင်းမယ်
            if self.check_winner(player_hand, dealer_hand):
                continue

        print()
        print("Final Results")
        print("Your hand: ", player_hand_value)
        print("Dealer's hand: ", dealer_hand_value)
        self.check_winner(player_hand, dealer_hand, True)

        print(f"Your wins => {self.player_wins} , Dealer wins => {self.dealer_wins}")

        print("\nThanks for Playing!")

    def check_winner(self, player_hand, dealer_hand, game_over=False):
        if not game_over:  # ? game end ဖြစ်ပြီလား ဆိုတာစစ်တာ | ဒီCondition က 21 ထပ်များသွားပြီလားရယ် Blackjack ဖြစ်လားမဖြစ်လားပဲ စစ်တာ
            if player_hand.get_value() > 21:
                print(f"You busted with {player_hand.get_value()}. Dealer wins! 😭 ")
                self.dealer_wins += 1
                return True
            elif dealer_hand.get_value() > 21:
                print(f"Dealer busted with {dealer_hand.get_value()}. You wins! 😄 ")
                self.player_wins += 1
                return True
            elif dealer_hand.is_blackjack() and player_hand.is_blackjack():
                print("Both players have blackjack! Tie! 😓 ")
                return True
            elif player_hand.is_blackjack():
                print("You have blackjack. You win! 😄 ♠️")
                self.player_wins += 1
                return True
            elif dealer_hand.is_blackjack():
                print("Dealer have blackjack. Dealer win! 😭 ♠️")
                self.dealer_wins += 1
                return True
            return False
        else:
            if player_hand.get_value() > dealer_hand.get_value():
                print("\nYou win! 😄 ")
            elif player_hand.get_value() == dealer_hand.get_value():
                print("\nTie")
            else:
                print("\nDealer win! 😭 ")

            return True
        return False


g = Game()
g.play()
