"""
Created on 19/08/2016

@author: AndrewM
"""
import doctest
from InterpreterAssignment import HTMLParser
from InterpreterAssignment import Product
from InterpreterAssignment import FileHandler

class Controller:
    """
    classdocs

    """
    # instances of Product
    #products = set()
    products = []
    # object counterparts of product
    #product_object = frozenset()
    
    def __init__(self, the_html_parser, the_command_interpreter, the_file_handler):
        '''
        Constructor
        '''
        self.my_html_parser = the_html_parser
        # self.my_product = the_product
        self.my_command_intepreter = the_command_interpreter
        self.my_file_handler = the_file_handler
        
    def go(self):
        self.my_command_intepreter.set_controller(self)
            # print("Dollars: " + str(price[0]) + " Cents " + str(price[1]))
        # start the CMD here, no more code will run until exiting.
        self.my_command_intepreter.cmdloop()
        # TESTING, NEED SOME TYPE OF VIEW FOR PRINTING
#         for i in range(len(self.products)):
#             print(self.products[i].get_description())
#             print(self.products[i].get_price())

    # Called by CommandInterpreter. 
    def save_data(self):
        # save the products to the database, if they exist
        if len(self.products) > 0:
            #objects = []
            #for product in self.products:
                #objects.append(product.get_object())
                #print(objects)
            self.my_file_handler.write_database(self.products)
        else:
            print("There are no products to save")
    # add unique 
    def load_data(self):
        # save existing descriptions in a list, so that they can be compared with
        # loaded descriptions to determine if they already exist.
        descriptions = []
        for product in self.products:
            descriptions.append(product.get_description())
        # for every instance of product saved, load it, get it's object data, then store it.
        loaded_data = self.my_file_handler.read_database()
        if loaded_data is not None:
            for loaded_product in loaded_data:
                # if the description is not found, it's not in the list, add it.
                if loaded_product.get_description() not in descriptions:
                    self.products.append(loaded_product)
            print(str(len(self.products)))
        
    def set_db_path(self, the_path):
        self.my_file_handler.set_path(the_path)
        
    def get_db_path(self):
        print(self.my_file_handler.get_db_path())
        
    def scrape_data(self):
        self.my_html_parser.collect_data()
        web_data = self.my_html_parser.get_data()
        date = web_data["date"]
        # used to verify repeat descriptions are not being added.
        descriptions = []
        # if there are existing products, add the descriptions to list.
        if len(self.products) > 0:
            for product in self.products:
                descriptions.append(product.get_description())
        # sort through the scrapped data and
        for i in range(len(web_data["descriptions"])):
            # if the description isn't already saved, save it.
            if web_data["descriptions"][i] not in descriptions:
                desc = web_data["descriptions"][i]
                price = web_data["prices"][i]
                link = web_data["links"][i]
                self.products.append(Product.Product(desc,price[0],price[1],link,date))

    def display_data(self):
        if len(self.products) > 0:
            for product in self.products:
                print(product.get_object())
        else:
            print("No products to display try loading or scraping")
# todo: write a function covering the functionality of
# building up descriptions, this is used in 2 places
# currently. 

# todo: add functionality which allows the incoming data
# to overwrite old data, should the user do a certain flag
# if the flag returns true, check if description exists if
# it exists, delete the old one, add the new one.