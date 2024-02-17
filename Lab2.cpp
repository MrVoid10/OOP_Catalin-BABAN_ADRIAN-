#include <iostream>
#include <string>
#include <list>
#include <fstream>
#include <sstream>

# define SAVE "University.txt"
using namespace std;

void Pause(){
  cout << "\nPress Enter to continue...";
  cin.ignore();
  getchar();
}

enum StudyField {
  MECHANICAL_ENGINEERING,
  SOFTWARE_ENGINEERING,
  FOOD_TECHNOLOGY,
  URBANISM_ARCHITECTURE,
  VETERINARY_MEDICINE
};

class Student {
private:
  string FirstName, LastName, Email;
  string EnrollmentDate, DateOfBirth; // It's pain to deal with c date type
  bool IsGraduated;

public:
  Student(string first, string last, string email, string enrollment, string dob)
      : FirstName(first), LastName(last), Email(email), EnrollmentDate(enrollment), DateOfBirth(dob), IsGraduated(false) {}

  Student(string first, string last, string email, string enrollment, string dob,bool grad)
      : FirstName(first), LastName(last), Email(email), EnrollmentDate(enrollment), DateOfBirth(dob), IsGraduated(grad) {}

  void Print_Info() { cout << '\n'<< FirstName << '|' << LastName << '|' << Email << '|' << EnrollmentDate << '|'
    << DateOfBirth;}

  const string& GetFirstName(){return FirstName;}
  const string& GetLastName(){return LastName;}
  const string& GetEmail() { return Email; }
  const string& GetEnrollmentDate() { return EnrollmentDate; }
  const string& GetDateOfBirth() { return DateOfBirth; }
  const bool GetIsGraduated() { return IsGraduated; }

  void Graduate() { IsGraduated = true; }
};

class Faculty {
private:
  string Name, Abreviation;
  list<Student> students;
  StudyField studyfield;

public:
  Faculty(string name, string abbreviation, StudyField field)
      : Name(name), Abreviation(abbreviation), studyfield(field) {}

  const string GetName() { return Name; }

  const string GetAbreviation() { return Abreviation; }

  void AddStudent(const Student& student) {
    students.push_back(student);
  }

  list<Student>& GetStudents() { return students; }

  StudyField GetStudyField() { return studyfield; }

  void DisplayStudents() {
    cout << "Students enrolled in " << Name << " faculty:\n";
    for ( auto& student : students) {
      student.Print_Info();
    }
    cout << endl;
  Pause();}

  void DisplayGraduates() {
    cout << "Graduates from " << Name << " faculty:\n";
    for ( auto& student : students) {
      if (student.GetIsGraduated()) {
        student.Print_Info();
      }
    }
    cout << endl;
  Pause();}

  bool CheckStudent(const string& email) {
    for ( auto& student : students) {
      if (student.GetEmail() == email) {
        return true;
      }
    }
    return false;
  }

  void GraduateStudent(const string& email) {
    for (auto& student : students) {
      if (student.GetEmail() == email) {
        student.Graduate();
        cout << student.GetFirstName() << ' ' << student.GetLastName() << " graduated from " << Name << " faculty.\n";
        return;
      }
    }
    cout << "Student with email '" << email << "' not found in " << Name << " faculty.\n";
  }
};

class University {
  //private: list<Faculty> faculties;

  public:list<Faculty> faculties;
    void CreateFaculty(string name, string abbreviation, StudyField field) {
      faculties.push_back(Faculty(name, abbreviation, field));
    }

    Faculty *FindFacultyByStudentEmail(const string &email) {
      for (auto &faculty : faculties) {
        if (faculty.CheckStudent(email)) {
          return &faculty;
        }
      }
      return nullptr;
    }

    void DisplayFaculties() {
      cout << "University Faculties:\n";
      for (auto &faculty : faculties) {
        cout << "- " << faculty.GetAbreviation() << " Faculty: " << faculty.GetName() << endl;
      }
      Pause();
      cout << endl;
    }

    void DisplayFacultiesByField(StudyField field) {
      cout << "Faculties in " << field << " field:\n";
      for (auto &faculty : faculties) {
        if (faculty.GetStudyField() == field) {
          cout << "- " << faculty.GetAbreviation() << " Faculty: " << faculty.GetName() << endl;
        }
      }
      Pause();
      cout << endl;
    }

    void DisplayStudentsInFaculty(const string &abbreviation) {
      for (auto &faculty : faculties) {
        if (faculty.GetAbreviation() == abbreviation) {
          faculty.DisplayStudents();
          return;
        }
      }
      cout << "Faculty with abbreviation '" << abbreviation << "' not found!\n";
    }

    void DisplayGraduatesInFaculty(const string &abbreviation) {
      for (auto &faculty : faculties) {
        if (faculty.GetAbreviation() == abbreviation) {
          faculty.DisplayGraduates();
          return;
        }
      }
      cout << "Faculty with abbreviation '" << abbreviation << "' not found!\n";
    }

    list<Faculty> &GetFaculties() {
      return faculties;
    }
};

class FileManager {
  public:
    static void SaveUniversityData(const string &filename, University &university) {///ceva probleme cu outputul
      ofstream outfile(filename);
      if (outfile.is_open()) {
        for (auto &faculty : university.GetFaculties()) {
          outfile << faculty.GetName() << "|" << faculty.GetAbreviation() << "|" << faculty.GetStudyField() << endl;
          for (auto &student : faculty.GetStudents()) {
            outfile << student.GetFirstName() << "|" << student.GetLastName() << "|" << student.GetEmail()
            << "|" << student.GetEnrollmentDate() << "|" << student.GetDateOfBirth() << "|" << student.GetIsGraduated() << endl;
          }
          outfile << endl; // Separate faculties with an empty line
        }
        cout << "University data saved successfully!\n";
      } else {
        cout << "Unable to open file for saving!\n";
      }
      outfile.close();
    }

    static void LoadUniversityData(const string &filename, University &university) { ///probleme cu inputul
      ifstream infile(filename);
      if (infile.is_open()) {
        string line;
        while (getline(infile, line)) {
          string name, abbreviation;
          int field;
          stringstream ss(line);
          getline(ss, name, '|');
          getline(ss, abbreviation, '|');
          ss >> field;
          university.CreateFaculty(name, abbreviation, static_cast<StudyField>(field));

          while (getline(infile, line) && !line.empty()) {
            stringstream ss2(line);
            string first, last, email,enroll,birth;
            bool isGraduated = false;
            getline(ss2, first, '|');
            getline(ss2, last, '|');
            getline(ss2, enroll, '|');
            getline(ss2, birth, '|');
            ss2 >> isGraduated;
            university.GetFaculties().back().AddStudent(Student(first, last, email, enroll, birth,isGraduated));
          }
        }
        cout << "University data loaded successfully!\n";
      } else {
        cout << "Unable to open file for loading!\n";
      }
      infile.close();
    }
};


int main() {
  University tum;
  FileManager::LoadUniversityData(SAVE,tum);
  int choice;

  do {
    system("CLS");
    cout << "TUM Board Menu:\n"
            "1. Faculty Operations\n"
            "2. General Operations\n"
            "0. Exit\n"
            "Enter your choice: ";
    cin >> choice;
    system("CLS");

    switch (choice) {
      case 1: { // Faculty Choice
        int facultyChoice;
        cout << "Faculty Operations:\n"
                "1. Create and assign a student to a faculty\n"
                "2. Graduate a student from a faculty\n"
                "3. Display current enrolled students\n"
                "4. Display graduates\n"
                "5. Check if a student belongs to a faculty\n"
                "0. Return to the Board Menu\n"
                "Enter your choice: ";
        cin >> facultyChoice;
        system("CLS");

        switch (facultyChoice) {// Faculty choice
          case 1: {
            string first, last, email, enrollment, dob;
            cout << "Enter student first name: ";
            cin >> first;
            cout << "Enter student last name: ";
            cin >> last;
            cout << "Enter student email: ";
            cin >> email;
            cout << "Enter student enrollment date: ";
            cin >> enrollment;
            cout << "Enter student date of birth: ";
            cin >> dob;
            system("CLS");

            Student student(first, last, email, enrollment, dob);

            string abbreviation;
            cout << "Enter the abbreviation of the faculty: ";
            cin >> abbreviation;
            system("CLS");

            bool facultyFound = false;
            for (auto& f : tum.faculties) {
              if (f.GetAbreviation() == abbreviation) {
                f.AddStudent(student);
                cout << "Student added to " << f.GetName() << " faculty.\n";
                facultyFound = true;
                break;
              }
            }

            if (!facultyFound) {
              cout << "Faculty with abbreviation '" << abbreviation << "' not found!\n";
            }
            break;
          }
          case 2: {
            string email;
            cout << "Enter student email to graduate: ";
            cin >> email;
            system("CLS");

            Faculty* faculty = tum.FindFacultyByStudentEmail(email);
            if (faculty != nullptr) {
              faculty->GraduateStudent(email);
            } else {
              cout << "Student with email '" << email << "' not found in any faculty.\n";
            }
            break;
          }
          case 3: {
            string abbreviation;
            cout << "Enter faculty abbreviation to display current enrolled students: ";
            cin >> abbreviation;
            tum.DisplayStudentsInFaculty(abbreviation);
            break;
          }
          case 4: {
            string abbreviation;
            cout << "Enter faculty abbreviation to display graduates: ";
            cin >> abbreviation;
            tum.DisplayGraduatesInFaculty(abbreviation);
            break;
          }
          case 5: {
            string email;
            cout << "Enter student email to check: ";
            cin >> email;
            system("CLS");

            Faculty* faculty = tum.FindFacultyByStudentEmail(email);
            if (faculty != nullptr) {
              cout << "Student with email '" << email << "' belongs to " << faculty->GetName() << " faculty.\n";
            } else {
              cout << "Student with email '" << email << "' not found in any faculty.\n";
            }
            break;
          }
          case 0: {break;}
          default:
            cout << "Invalid choice!\n";
        }break;}
      case 2: { // General Choice
        int generalChoice;
        cout << "General Operations:\n"
                "1. Create a new faculty\n"
                "2. Search what faculty a student belongs to\n"
                "3. Display University faculties\n"
                "4. Display faculties belonging to a field\n"
                "0. Return to the Board Menu\n"
                "Enter your choice: ";
        cin >> generalChoice;
        system("CLS");

        switch (generalChoice) { // General Choice
          case 1: {
            string name, abbreviation;
            int field;
            cout << "Enter faculty name: ";
            cin >> name;
            cout << "Enter faculty abbreviation: ";
            cin >> abbreviation;
            cout << "Enter field (0-4): ";
            cin >> field;
            tum.CreateFaculty(name, abbreviation, static_cast<StudyField>(field));
            cout << "Faculty created successfully!\n";
          break;}
          case 2: {
            string email;
            cout << "Enter student email to search: ";
            cin >> email;
            system("CLS");

            Faculty* faculty = tum.FindFacultyByStudentEmail(email);
            if (faculty != nullptr) {
              cout << "Student with email '" << email << "' belongs to " << faculty->GetName() << " faculty.\n";
            } else {
              cout << "Student with email '" << email << "' not found in any faculty.\n";
            }
            Pause();
          break;}
          case 3: {
            tum.DisplayFaculties();
          break;}
          case 4: {
            int field;
            cout << "Enter the field (0-4): ";
            cin >> field;
            tum.DisplayFacultiesByField(static_cast<StudyField>(field));
            break;}
          case 0: {break;}
          default:
            cout << "Invalid choice!\n";
        }
      break;}
      case 0:   // Exiting the Program
        cout << "Exiting...\n";
        FileManager::SaveUniversityData(SAVE,tum);
        break;
      default:
        cout << "Invalid choice!\n";
    }
  } while (choice);

  return 0;
}
