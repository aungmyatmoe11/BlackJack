import random
import tkinter as tk
from tkinter import messagebox

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank['rank']} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = []
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

    def shuffle(self):
        if len(self.cards) > 1:
            random.shuffle(self.cards)

    def deal(self, number):
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

        if has_ace and self.value > 21:
            self.value -= 10

    def get_value(self):
        self.calculate_value()
        return self.value

    def is_blackjack(self):
        return self.get_value() == 21

    def display(self, show_all_dealer_cards=False):
        hand_value = ""
        for index, card in enumerate(self.cards):
            if index == 0 and self.dealer and not show_all_dealer_cards and not self.is_blackjack():
                hand_value += "hidden, "
            else:
                hand_value += str(card) + ", "
        return hand_value.strip(", ")

class Game:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Blackjack Game")

        self.deck = Deck()
        self.deck.shuffle()

        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)

        self.setup_gui()
        self.new_game()

    def setup_gui(self):
        self.dealer_label = tk.Label(self.window, text="Dealer's hand: ", font=("Arial", 14))
        self.dealer_label.pack()

        self.dealer_hand_label = tk.Label(self.window, text="", font=("Arial", 14))
        self.dealer_hand_label.pack()

        self.player_label = tk.Label(self.window, text="Your hand: ", font=("Arial", 14))
        self.player_label.pack()

        self.player_hand_label = tk.Label(self.window, text="", font=("Arial", 14))
        self.player_hand_label.pack()

        self.hit_button = tk.Button(self.window, text="Hit", command=self.hit)
        self.hit_button.pack(side=tk.LEFT, padx=20)

        self.stand_button = tk.Button(self.window, text="Stand", command=self.stand)
        self.stand_button.pack(side=tk.RIGHT, padx=20)

    def new_game(self):
        self.player_hand = Hand()
        self.dealer_hand = Hand(dealer=True)
        for i in range(2):
            self.player_hand.add_card(self.deck.deal(1))
            self.dealer_hand.add_card(self.deck.deal(1))
        self.update_gui()
        if self.check_winner():
            return

    def hit(self):
        self.player_hand.add_card(self.deck.deal(1))
        self.update_gui()
        if self.check_winner():
            return

    def stand(self):
        dealer_hand_value = self.dealer_hand.get_value()
        while dealer_hand_value < 17:
            self.dealer_hand.add_card(self.deck.deal(1))
            dealer_hand_value = self.dealer_hand.get_value()
        self.update_gui(show_all_dealer_cards=True)
        self.check_winner(game_over=True)

    def update_gui(self, show_all_dealer_cards=False):
        self.dealer_hand_label.config(text=self.dealer_hand.display(show_all_dealer_cards))
        self.player_hand_label.config(text=self.player_hand.display())
        if not show_all_dealer_cards:
            self.dealer_label.config(text="Dealer's hand: hidden")
        else:
            self.dealer_label.config(text=f"Dealer's hand: {self.dealer_hand.get_value()}")

    def check_winner(self, game_over=False):
        if not game_over:
            if self.player_hand.get_value() > 21:
                messagebox.showinfo("Game Over", f"You busted with {self.player_hand.get_value()}. Dealer wins!")
                return True
            elif self.dealer_hand.get_value() > 21:
                messagebox.showinfo("Game Over", f"Dealer busted with {self.dealer_hand.get_value()}. You win!")
                return True
            elif self.dealer_hand.is_blackjack() and self.player_hand.is_blackjack():
                messagebox.showinfo("Game Over", "Both players have blackjack! It's a tie!")
                return True
            elif self.player_hand.is_blackjack():
                messagebox.showinfo("Game Over", "You have blackjack! You win!")
                return True
            elif self.dealer_hand.is_blackjack():
                messagebox.showinfo("Game Over", "Dealer has blackjack! Dealer wins!")
                return True
            return False
        else:
            if self.player_hand.get_value() > self.dealer_hand.get_value():
                messagebox.showinfo("Game Over", "You win!")
            elif self.player_hand.get_value() == self.dealer_hand.get_value():
                messagebox.showinfo("Game Over", "It's a tie!")
            else:
                messagebox.showinfo("Game Over", "Dealer wins!")
            return True

if __name__ == "__main__":
    game = Game()
    game.window.mainloop()
