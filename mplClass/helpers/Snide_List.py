#!/usr/bin/env python
import numpy as N

class Famous_Quotes():
    def __init__(self, parent = None):
        self.snide_list = []
        self.snide_list.append("Wutchu talkin' 'bout fool?!")
        self.snide_list.append("Try again slick")
        self.snide_list.append("O'Doyle Rules!!!!")
        self.snide_list.append("You smell take a bath")
        self.snide_list.append("Qieras Taco Bell?")
        self.snide_list.append("Where's the Beef?")
        self.snide_list.append("Yo Mama")
        self.snide_list.append("Your actions have been logged and reported to DHS")
        self.snide_list.append("U-G-L-Y")
        self.snide_list.append("You know you're a teacher when you say 2, write 3, and mean 4.--Ronald Anstrom, high school teacher, Underwood, N.D. 1974")
        self.snide_list.append("Research is what I am doing when I don't know what I am doing.-- Werner von Braun")
        self.snide_list.append("Learn from yesterday, live for today, look to tomorrow, rest this afternoon.-- Snoopy")
        self.snide_list.append("The great thing about being imperfect is the joy it brings others.-- Sign outside Lake Agassiz Jr. High School, Fargo, N.D.")
        self.snide_list.append("It is unworthy of excellent men to lose hours like slaves in the labor of calculation which could be safely relegated to anyone else if a machine were used.-- G. W. von Leibniz")
        self.snide_list.append("The mind is not a vessel to be filled but a fire to be kindled.-- Plutarch")
        self.snide_list.append("Why do you believe the sun will rise tomorrow?-- Bertrand Russell")
        self.snide_list.append("Good sense about trivialities is better than nonsense about things that matter.-- Max Beerbohm")
        self.snide_list.append("Nature will tell you a direct lie if she can.-- Charles Darwin")
        self.snide_list.append("You shouldn't let people drive you crazy when you know it's within walking distance.")
        self.snide_list.append("Sometimes the fool who rushes in gets the job done.-- Al Bernstein")
        self.snide_list.append("If at first you don't succeed, try looking in the wastebasket for the directions.")
        self.snide_list.append("It takes greater character to carry off good fortune than bad.-- French proverb.")
        self.snide_list.append("Laws of programming definition: a working program is one that has only unobserved bugs.")
        self.snide_list.append("A leading authority is anyone who has guessed right more than once.-- Frank A. Clark")
        self.snide_list.append("My description of experience is not what happens to a man. Experience is what a man does with what happens to him.-- Chuck Knox, Seattle Seahawks, 1985")
        self.snide_list.append("I have not failed, I have only discovered 10,000 ways that didn't work.-- Thomas A. Edison")
        self.snide_list.append("Mathematics is the art of giving the same name to different things.-- H. Poincare")
    
    def return_quote(self):
        return self.snide_list[N.random.randint(0, len(self.snide_list))]
        
        


def getQuote():
    quote_list = Famous_Quotes()
    return quote_list.return_quote()
    