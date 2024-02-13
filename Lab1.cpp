#include <iostream>
#include <vector>

class Book {
public:
  Book(std::string title, std::string author, std::string isbn)
    : title(title), author(author), isbn(isbn) {}

  void displayInfo() const {
    std::cout << "\nTitle:  " << title;
    std::cout << "\nAuthor: " << author;
    std::cout << "\nISBN:   " << isbn << '\n';
  }

private:
  std::string title,author,isbn;
};

class Library {
public:
  // Add a book to the library
  void addBook(const Book& book) {
    books.push_back(book);
  }
  void removeBook(const std::string& title) {
        for (auto it = books.begin(); it != books.end(); ++it) {
            if (it->getTitle() == title) {
                books.erase(it);
                std::cout << "Book '" << title << "' removed from the library.\n";
                return;
            }
        }
        std::cout << "Book '" << title << "' not found in the library.\n";
    }  
  // Display all books in the library
  void display_All_Books() const {
    for (const Book& book : books) {
      book.displayInfo();
      std::cout << "------------------------\n";
    }
  }

private:
  std::vector<Book> books;
};

Book User_Input_Book() {
  std::string title, author, isbn;

  std::cout << "\nTitle: ";
  std::getline(std::cin, title);

  std::cout << "Author: ";
  std::getline(std::cin, author);

  std::cout << "ISBN: ";
  std::getline(std::cin, isbn);

return Book(title, author, isbn);}

int main() {
  int n; Library library;
  std::cout << "How many books to input: ";
  std::cin >> n;

  std::cin.ignore(); // pentru ca probleme cu autorul la prima carte
  std::cout << "Enter book details:\n";
  for(int i=0;i<n;i++){ // adauga carti
    std::cout<< "\nBook["<< i+1<<"]:";
    Book Temp_book = User_Input_Book();
    library.addBook(Temp_book);
  }

    // Displaying all books in the library
    system("cls");
    std::cout << "Library Contents:\n";
    library.display_All_Books();

  std::string bookToRemove;
    std::cout << "\nEnter the title of the book to remove: ";
    std::getline(std::cin, bookToRemove);
    library.removeBook(bookToRemove);
return 0;}
