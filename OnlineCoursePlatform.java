/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package pkg25mca156;

/**
 *
 * @author 1STUDENT32
 */

import java.util.*;

class InvalidNameException extends Exception {
    public InvalidNameException(String message) {
        super(message);
    }
}

class EmptyCourseListException extends Exception {
    public EmptyCourseListException(String message) {
        super(message);
    }
}

abstract class Person {
    public String personID, name;

    public Person(String personID, String name) throws InvalidNameException {
        if (name == null || name.isEmpty()) {
            throw new InvalidNameException("NAME IS INVALID");
        }
        this.personID = personID;
        this.name = name;
    }

    abstract void showRole();
}

class Student extends Person {
    private ArrayList<String> ecou;

    Student(String personID, String name, ArrayList<String> ecou) throws EmptyCourseListException, InvalidNameException {
        super(personID, name);
        if (ecou == null || ecou.isEmpty()) {
            throw new EmptyCourseListException("ENROLLED COURSE IS EMPTY");
        }
        this.ecou = ecou;
    }

    void printInfo() {
        System.out.println("ID of Student is: " + personID);
        System.out.println("Name of Student is: " + name);
        System.out.println("Courses enrolled are: " + ecou);
    }

    void showRole() {
        System.out.println("THIS IS STUDENT ROLE");
    }
}

class Instructor extends Person {
    private ArrayList<String> tcou;

    Instructor(String personID, String name, ArrayList<String> tcou) throws EmptyCourseListException, InvalidNameException {
        super(personID, name);
        if (tcou == null || tcou.isEmpty()) {
            throw new EmptyCourseListException("TEACHING COURSE IS EMPTY");
        }
        this.tcou = tcou;
    }

    void printInfo() {
        System.out.println("ID of Instructor is: " + personID);
        System.out.println("Name of Instructor is: " + name);
        System.out.println("Courses taught are: " + tcou);
    }

    void showRole() {
        System.out.println("THIS IS INSTRUCTOR ROLE");
    }
}

public class OnlineCoursePlatform {
    public static void main(String[] args) throws EmptyCourseListException, InvalidNameException {
            ArrayList<String> enrolledCourses = new ArrayList<>(Arrays.asList("JAVA", "ASP.NET"));
            ArrayList<String> teachingCourses = new ArrayList<>(Arrays.asList("JAVA"));

            Student s = new Student("25MCA156", "RIYA", enrolledCourses);
            Instructor i = new Instructor("A101", "KK", teachingCourses);

            s.showRole();
            s.printInfo();

            i.showRole();
            i.printInfo();
    }
}

