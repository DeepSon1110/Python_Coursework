import read
import write
def menu():
  """Display all the available options"""
  
  print("""
        Welcome to the BRJ Furniture
          Choose an Option 
          1.Display Available Furnitures
          2.Buy Furnitures
          3.Sell Furnitures
          4.Exit
                """)

def main():
  
  """
  This is the main function that runs the program:
  -This function read the furniture from a file.
  -Display the menu and ask user to input value.
  -Calls appropriate function according to user's input.
  -Loop runs until user choose to exit.
  """
  
  #from the read file load the furniture items
  furniture_list = read.read_file()
  
  while True:
    #Display menu option
    menu()
    
    # getting user input
    choose = input("Enter your choice: ")
    
    if choose == '1':
      #Displays the list of available furnitures
      read.display_available_furniture(furniture_list)
      
    elif choose == '2':
      #Buy furniture and update list
      write.buy_furniture()
      
    elif choose =='3':
      #Sell furniture and update list
      write.sell_furniture()
        
    elif choose =='4':
      #Exiting the Program
      print("Thank you for choosing BRJ Furniture")
      break
    else:
      #Handling invlid input by the user
      print("Invalid choice.Please input a valid option.")
      
#Check
if __name__ == '__main__':
  main()

