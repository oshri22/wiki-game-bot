import requests
from bs4 import BeautifulSoup
import sys
import threading

class thread_for_with(threading.Thread):

    def __init__(self, func, args):
        super().__init__(target = func, args =args )
        self.func_to_run = func 

    def __enter__(self):
        return self

    def __exit__(self,*kargs):
        #pass
        self.join()

class bot_player:

    def __init__(self):
        temp = input("Enter the start page (random for random starting page) ")
        self.start_page = "Special:Random" if temp == "random" else temp
        self.end_page = input("Enter the ending page (It can't be random) ").replace(" ", "_")
        self.curr_url = "https://en.wikipedia.org/wiki/%s"
        self.found = False

        if requests.get(self.curr_url % self.start_page).status_code != 200:
            print("Coudnt find the starting page please try again")

        elif requests.get(self.curr_url % self.end_page).status_code != 200:
            print("Coudnt find the ending page please try again")
        else:
           self.solve(0,[],self.start_page)
            
            
        
    def solve(self, count, visited_list, curr_page):
        if self.found:
            return 

        print(f"in layer {count}")

        visited_list.append(curr_page)
        c_page = requests.get(self.curr_url % curr_page)

        if c_page.status_code != 200:
            return 

        soap = BeautifulSoup(c_page.text, 'html.parser')

        for i in soap.find_all("div", {"class":"mw-body-content"}):
            linkes = [a['href'] for a in i.find_all("a", href = True)]

        for i in linkes:
            t = thread_for_with(self.condition, (i, visited_list,count,))
            with t:
                t.start()



    def condition(self,i, visited_list, count):
        if not i.startswith ("/wiki/") or i.endswith(".jpg"):
            return 
        
        page_name = i.split("/")[2]
        if ":" in page_name or page_name in visited_list:
            return 

        if count == 6:
            return 
    
        if page_name == self.end_page:
            visited_list.append(self.end_page)
            print(f"Found a way\n {' -> '.join(visited_list)}")
            self.found = True
            return 

        else:
            """ t = thread_for_with(self.solve, (count+1, visited_list, page_name,))
            with t:
                t.start()  """
            self.solve(count+1, visited_list, page_name)
            try:
                visited_list.pop(-1)
            except IndexError:
                pass
            return 

if __name__ == "__main__":
    bot = bot_player()
