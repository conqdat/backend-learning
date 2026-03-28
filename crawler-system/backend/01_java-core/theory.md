---
# Trail: Learning the Java Language

> Source: https://docs.oracle.com/javase/tutorial/java/index.html

 A browser with JavaScript enabled is required for this page to operate properly.


Documentation





 The Java™ Tutorials




[Home Page](../index.html)

[« Previous](../index.html)
 •
 [Trail](./TOC.html)
 •
 [Next »](./concepts/index.html)

The Java Tutorials have been written for JDK 8. Examples and practices described in this page don't take advantage of improvements introduced in later releases and might use technology no longer available.
See [Dev.java](https://dev.java/learn/) for updated tutorials taking advantage of the latest releases.
See [Java Language Changes](https://docs.oracle.com/pls/topic/lookup?ctx=en/java/javase&id=java_language_changes) for a summary of updated language features in Java SE 9 and subsequent releases.
See [JDK Release Notes](https://www.oracle.com/technetwork/java/javase/jdk-relnotes-index-2162236.html) for information about new features, enhancements, and removed or deprecated options for all JDK releases.
# Trail: Learning the Java Language

This trail covers the fundamentals of programming in the Java programming language.

[![trail icon](../images/javaIcon.gif) **Object-Oriented Programming Concepts**](concepts/index.html) teaches you the core concepts behind object-oriented programming: objects, messages, classes, and inheritance. This lesson ends by showing you how these concepts translate into code. Feel free to skip this lesson if you are already familiar with object-oriented programming.

[![trail icon](../images/javaIcon.gif) **Language Basics**](nutsandbolts/index.html) describes the traditional features of the language, including variables, arrays, data types, operators, and control flow.

[![trail icon](../images/javaIcon.gif) **Classes and Objects**](javaOO/index.html) describes how to write the classes from which objects are created, and how to create and use the objects.

[![trail icon](../images/javaIcon.gif) **Annotations**](annotations/index.html) are a form of metadata and provide information for the compiler. This lesson describes where and how to use annotations in a program effectively.

[![trail icon](../images/javaIcon.gif) **Interfaces and Inheritance**](IandI/index.html) describes interfaceswhat they are, why you would want to write one, and how to write one. This section also describes the way in which you can derive one class from another. That is, how a *subclass* can inherit fields and methods from a *superclass*. You will learn that all classes are derived from the `Object` class, and how to modify the methods that a subclass inherits from superclasses.

[![trail icon](../images/javaIcon.gif) **Numbers and Strings**](data/index.html) This lesson describes how to use `Number` and `String` objects The lesson also shows you how to format data for output.

[![trail icon](../images/javaIcon.gif) **Generics**](generics/index.html) are a powerful feature of the Java programming language. They improve the type safety of your code, making more of your bugs detectable at compile time.

[![trail icon](../images/javaIcon.gif) **Packages**](package/index.html) are a feature of the Java programming language that help you to organize and structure your classes and their relationships to one another.

[« Previous](../index.html)
 •
 [TOC](./TOC.html)
 •
 [Next »](./concepts/index.html)

---

[About Oracle](https://www.oracle.com/corporate/) |
[Contact Us](https://www.oracle.com/corporate/contact/) |
[Legal Notices](https://www.oracle.com/legal/) |
[Terms of Use](https://www.oracle.com/legal/terms.html) |
[Your Privacy Rights](https://www.oracle.com/legal/privacy/)

[Copyright © 1995, 2024 Oracle and/or its affiliates. All rights reserved.](http://www.oracle.com/pls/topic/lookup?ctx=cpyr&id=en-US)

**Previous page:** Beginning of Tutorial

**Next page:** Object-Oriented Programming Concepts


---
# Lesson: Object-Oriented Programming Concepts

> Source: https://docs.oracle.com/javase/tutorial/java/concepts/index.html

 A browser with JavaScript enabled is required for this page to operate properly.


Documentation





 The Java™ Tutorials


[Hide TOC](javascript:toggleLeft())



Object-Oriented Programming Concepts
[What Is an Object?](object.html)
[What Is a Class?](class.html)
[What Is Inheritance?](inheritance.html)
[What Is an Interface?](interface.html)
[What Is a Package?](package.html)
[Questions and Exercises](QandE/questions.html)

**Trail:** Learning the Java Language


[Home Page](../../index.html)
 >
 [Learning the Java Language](../index.html)

[« Previous](../index.html) • [Trail](../TOC.html) • [Next »](object.html)

The Java Tutorials have been written for JDK 8. Examples and practices described in this page don't take advantage of improvements introduced in later releases and might use technology no longer available.
See [Dev.java](https://dev.java/learn/) for updated tutorials taking advantage of the latest releases.
See [Java Language Changes](https://docs.oracle.com/pls/topic/lookup?ctx=en/java/javase&id=java_language_changes) for a summary of updated language features in Java SE 9 and subsequent releases.
See [JDK Release Notes](https://www.oracle.com/technetwork/java/javase/jdk-relnotes-index-2162236.html) for information about new features, enhancements, and removed or deprecated options for all JDK releases.
# Lesson: Object-Oriented Programming Concepts

If you've never used an object-oriented programming language before, you'll need to learn a few basic concepts before you can begin writing any code. This lesson will introduce you to objects, classes, inheritance, interfaces, and packages. Each discussion focuses on how these concepts relate to the real world, while simultaneously providing an introduction to the syntax of the Java programming language.
## [What Is an Object?](object.html)

An object is a software bundle of related state and behavior. Software objects are often used to model the real-world objects that you find in everyday life. This lesson explains how state and behavior are represented within an object, introduces the concept of data encapsulation, and explains the benefits of designing your software in this manner.
## [What Is a Class?](class.html)

A class is a blueprint or prototype from which objects are created. This section defines a class that models the state and behavior of a real-world object. It intentionally focuses on the basics, showing how even a simple class can cleanly model state and behavior.
## [What Is Inheritance?](inheritance.html)

Inheritance provides a powerful and natural mechanism for organizing and structuring your software. This section explains how classes inherit state and behavior from their superclasses, and explains how to derive one class from another using the simple syntax provided by the Java programming language.
## [What Is an Interface?](interface.html)

An interface is a contract between a class and the outside world. When a class implements an interface, it promises to provide the behavior published by that interface. This section defines a simple interface and explains the necessary changes for any class that implements it.
## [What Is a Package?](package.html)

A package is a namespace for organizing classes and interfaces in a logical manner. Placing your code into packages makes large software projects easier to manage. This section explains why this is useful, and introduces you to the Application Programming Interface (API) provided by the Java platform.
## [Questions and Exercises: Object-Oriented Programming Concepts](QandE/questions.html)

Use the questions and exercises presented in this section to test your understanding of objects, classes, inheritance, interfaces, and packages.


[« Previous](../index.html)
 •
 [Trail](../TOC.html)
 •
 [Next »](object.html)

---

[About Oracle](https://www.oracle.com/corporate/) |
[Contact Us](https://www.oracle.com/corporate/contact/) |
[Legal Notices](https://www.oracle.com/legal/) |
[Terms of Use](https://www.oracle.com/legal/terms.html) |
[Your Privacy Rights](https://www.oracle.com/legal/privacy/)

[Copyright © 1995, 2024 Oracle and/or its affiliates. All rights reserved.](http://www.oracle.com/pls/topic/lookup?ctx=cpyr&id=en-US)

**Previous page:** Table of Contents

**Next page:** What Is an Object?


---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/javaOOPs/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)

---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/essential/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)

---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/collections/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)

---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/concurrency/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)

---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/uiswing/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)

---
# Lesson: Generics (Updated)

> Source: https://docs.oracle.com/javase/tutorial/java/generics/index.html

 A browser with JavaScript enabled is required for this page to operate properly.


Documentation





 The Java™ Tutorials


[Hide TOC](javascript:toggleLeft())



Generics (Updated)
[Why Use Generics?](why.html)
[Generic Types](types.html)
[Raw Types](rawTypes.html)
[Generic Methods](methods.html)
[Bounded Type Parameters](bounded.html)
[Generic Methods and Bounded Type Parameters](boundedTypeParams.html)
[Generics, Inheritance, and Subtypes](inheritance.html)
[Type Inference](genTypeInference.html)
[Wildcards](wildcards.html)
[Upper Bounded Wildcards](upperBounded.html)
[Unbounded Wildcards](unboundedWildcards.html)
[Lower Bounded Wildcards](lowerBounded.html)
[Wildcards and Subtyping](subtyping.html)
[Wildcard Capture and Helper Methods](capture.html)
[Guidelines for Wildcard Use](wildcardGuidelines.html)
[Type Erasure](erasure.html)
[Erasure of Generic Types](genTypes.html)
[Erasure of Generic Methods](genMethods.html)
[Effects of Type Erasure and Bridge Methods](bridgeMethods.html)
[Non-Reifiable Types](nonReifiableVarargsType.html)
[Restrictions on Generics](restrictions.html)
[Questions and Exercises](QandE/generics-questions.html)

**Trail:** Learning the Java Language


[Home Page](../../index.html)
 >
 [Learning the Java Language](../index.html)

[« Previous](../data/index.html) • [Trail](../TOC.html) • [Next »](why.html)

The Java Tutorials have been written for JDK 8. Examples and practices described in this page don't take advantage of improvements introduced in later releases and might use technology no longer available.
See [Dev.java](https://dev.java/learn/) for updated tutorials taking advantage of the latest releases.
See [Java Language Changes](https://docs.oracle.com/pls/topic/lookup?ctx=en/java/javase&id=java_language_changes) for a summary of updated language features in Java SE 9 and subsequent releases.
See [JDK Release Notes](https://www.oracle.com/technetwork/java/javase/jdk-relnotes-index-2162236.html) for information about new features, enhancements, and removed or deprecated options for all JDK releases.
# Lesson: Generics (Updated)

In any nontrivial software project, bugs are simply a fact of life. Careful planning, programming, and testing can help reduce their pervasiveness, but somehow, somewhere, they'll always find a way to creep into your code. This becomes especially apparent as new features are introduced and your code base grows in size and complexity.

Fortunately, some bugs are easier to detect than others. Compile-time bugs, for example, can be detected early on; you can use the compiler's error messages to figure out what the problem is and fix it, right then and there. Runtime bugs, however, can be much more problematic; they don't always surface immediately, and when they do, it may be at a point in the program that is far removed from the actual cause of the problem.

Generics add stability to your code by making more of your bugs detectable at compile time. After completing this lesson, you may want to follow up with the
[Generics](../../extra/generics/index.html) tutorial by Gilad Bracha.

[« Previous](../data/index.html)
 •
 [Trail](../TOC.html)
 •
 [Next »](why.html)

---

[About Oracle](https://www.oracle.com/corporate/) |
[Contact Us](https://www.oracle.com/corporate/contact/) |
[Legal Notices](https://www.oracle.com/legal/) |
[Terms of Use](https://www.oracle.com/legal/terms.html) |
[Your Privacy Rights](https://www.oracle.com/legal/privacy/)

[Copyright © 1995, 2024 Oracle and/or its affiliates. All rights reserved.](http://www.oracle.com/pls/topic/lookup?ctx=cpyr&id=en-US)

**Previous page:** Previous Lesson

**Next page:** Why Use Generics?


---
# JDK 26 Documentation

> Source: https://docs.oracle.com/javase/tutorial/java/lambda/index.html

Search

- [Help Center Home](/)

- [Home](index.html)
- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Guides](books.html)

---

- [Related Resources](related-resources.html)

![](sp_common/shared-images/1-java.png)
1. [Home](../../../../../index.html)
2. [Java](../../index.html)
3. [Java SE](../index.html)
4. [26](index.html)
# JDK 26 Documentation


## Home

[Java Components page](https://docs.oracle.com/javacomponents/index.html)

Looking for a different release? [Other releases](../index.html)
### Overview

- [Read Me](https://www.oracle.com/java/technologies/javase/jdk26-readme-downloads.html)
- [Release Notes](https://www.oracle.com/java/technologies/javase/26all-relnotes.html)
- [What's New](https://www.oracle.com/java/technologies/javase/26-relnote-issues.html
#NewFeature)

- [Migration Guide](/en/java/javase/26/migrate/getting-started.html)
- [Download the JDK](https://www.oracle.com/java/technologies/downloads/)
- [Installation Guide](/en/java/javase/26/install/overview-jdk-installation.html)
- [Version-String Format](/en/java/javase/26/install/version-string-format.html)
### Tools

- [JDK Tool Specifications](/en/java/javase/26/docs/specs/man/index.html)
- [JShell User's Guide](/en/java/javase/26/jshell/introduction-jshell.html)
- [JavaDoc Guide](/en/java/javase/26/javadoc/index.html)
- [Packaging Tool User's Guide](/en/java/javase/26/jpackage/packaging-overview.html)
### Language and Libraries

- [Language Updates](/en/java/javase/26/language/java-language-changes-release.html)
- [Core Libraries](/en/java/javase/26/core/java-core-libraries.html)
- [JDK HTTP Client](http://openjdk.java.net/groups/net/httpclient/)
- [Java Tutorials](https://dev.java/learn/)
- [Modular JDK](http://openjdk.java.net/projects/jigsaw/)
- [Flight Recorder API Programmerâs Guide](/en/java/javase/26/jfapi/why-use-jfr-api.html)
- [Internationalization Guide](/en/java/javase/26/intl/internationalization-overview.html)
### Specifications

- [API Documentation](/en/java/javase/26/docs/api/overview-summary.html)
- [Java Language Specification](/en/java/javase/26/docs/specs/jls/index.html)
- [Java Virtual Machine Specification](/en/java/javase/26/docs/specs/jvms/index.html)
- [Java Security Standard Algorithm Names](/en/java/javase/26/docs/specs/security/standard-names.html)
- [JAR File](/en/java/javase/26/docs/specs/jar/jar.html)
- [Java Native Interface (JNI)](/en/java/javase/26/docs/specs/jni/index.html)
- [JVM Tool Interface (JVM TI)](/en/java/javase/26/docs/specs/jvmti.html)
- [Serialization](/en/java/javase/26/docs/specs/serialization/index.html)
- [Java Debug Wire Protocol (JDWP)](/en/java/javase/26/docs/specs/jdwp/jdwp-spec.html)
- [Documentation Comment Specification for the Standard Doclet](/en/java/javase/26/docs/specs/javadoc/doc-comment-spec.html)
- [Other specifications](/en/java/javase/26/docs/specs/index.html)
### Security

- [Secure Coding Guidelines](https://www.oracle.com/java/technologies/javase/seccodeguide.html)
- [Security Guide](/en/java/javase/26/security/)
### HotSpot Virtual Machine

- [Java Virtual Machine Guide](/en/java/javase/26/vm/java-virtual-machine-technology-overview.html)
- [Garbage Collection Tuning](/en/java/javase/26/gctuning/introduction-garbage-collection-tuning.html)
### Manage and Troubleshoot

- [Troubleshooting Guide](/en/java/javase/26/troubleshoot/general-java-troubleshooting.html)
- [Monitoring and Management Guide](/en/java/javase/26/management/)
- [JMX Guide](/en/java/javase/26/jmx/introduction-jmx-technology.html)
### Client Technologies

- [JavaFX](/en/java/java-components/javafx/26/index.html)
- [Java Accessibility Guide](/en/java/javase/26/access/java-accessibility-overview.html)