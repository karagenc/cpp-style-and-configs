# C++ Style Guide

C++ is a very generic programming language. It is used in almost all disciplines one can think of, and there is no single standard coding style. On the contrary: Projects are very divergent in this regard.

This style brings best styles and conventions of cybersecurity, systems development, AI & scientific development, and flight software, aiming to unite programmers from different backgrounds. In addition to that, I took inspiration from my favorite programming languages: Rust, Go, and some good C & C++ repositories.

This style is oriented towards code reading. Writing code is secondary: Reading code takes much more time than writing it, and reading happens much more than writing, so this style guide is balanced more towards reading and understanding the code.

If the codebase you are working on already uses a different style or one of the styles below, do not use this style guide. Follow its own style guide or conventions. Some other style guides:
- [Unreal Engine Coding Standard](https://docs.unrealengine.com/en-US/epic-cplusplus-coding-standard-for-unreal-engine)
- [Qt Coding Style](https://wiki.qt.io/Qt_Coding_Style)
- [Linux Kernel Coding Style](https://www.kernel.org/doc/html/latest/process/coding-style.html)
- [Google Style Guide](https://google.github.io/styleguide/cppguide.html)

## `.clang-format`

There is a `.clang-format` file inside this directory that is configured for this style guide. Minimum supported `clang-format` version is choosen by looking at package version from Ubuntu and Debian repositories — because Ubuntu and Debian are non-rolling distros, and their packages are stable and older versions relative to other distros —, and `.clang-format` file is written to support that version and higher versions. Current minimum supported version is 14.

`clang-format` often requires to use a specific style option instead of leaving that to user. In those cases, sensible defaults were used.

## File names and extensions

Casing of file names should be `snake_case`. If project includes grapchical user interface (GUI) specific source files, those files can be named `PascalCase`. **Rationale:** `PascalCase` is used for GUI source files (e.g. Svelte, Vue, and React). Thus using `snake_case` by default, and using `PascalCase` for GUI-specific source files will make it easier to distinguish GUI and non-GUI source files.

Use `.c` for C source files, and use `.cpp` for C++ source files.

Prefer to use the `.h` extension for C and C++ header files rather than `.hpp`. The `.hpp` extension carries two implications: firstly, it suggests a combination of two elements, "header" (`.h`) and "source" (`pp` from `.cpp`), thus, `.hpp` should be used for header-only files. Secondly, `.hpp` implies specificity to C++. Use `.hpp` if you require a clear differentiation between C and C++ header files. Otherwise, for both C and C++ header files, use the `.h` extension.

## Style

### Use double quotes for header includes

Default to use quotes instead of angle brackets for headers. Prefer to use angle brackets only with system headers. When confronted with project-local (`project/include/x.h`) and system-wide (`/usr/include/x.h`), with double quotes, compiler will choose project-local header file, saving the programmer a lot of headaches.

**Rationale:** Consider this scenario: You built and installed a library — its headers too —, and you change the project-local header file `project/include/x.h`, but somehow your changes do not show up on tests. Guess why? Because you used angle brackets, and compiler preferred the older system-wide header, `/usr/include/x.h` over newer header, `project/include/x.h`.

### Include guard

Use include guard. Avoid `#pragma once`. See: https://stackoverflow.com/a/34884735

Use format `<PROJECT>_<DIR>_<FILE>_H` (Omit `src` and `include` directories.)

Example:
```c++
// foo/src/zar/tar.h
#ifndef FOO_ZAR_TAR_H
#define FOO_ZAR_TAR_H
#endif
```

### Indentation

Indent 4 spaces. Use spaces instead of tabs for indentation.

Indent preprocessor directives. Do not indent `case` labels of `switch` statements.

```c++
#ifdef USE_OPENGL
    #define GRAPHICS_API "OpenGL"
#else
    #define GRAPHICS_API "DirectX"
#endif

switch (GRAPHICS_API) {
case "OpenGL":
    // Initialize OpenGL.
    // ...
    break;
case "DirectX":
    // Initialize DirectX.
    // ...
    break;
default:
    // Invalid graphics API. Return an error.
    break;
}
```

**Rationale:** 4 spaces indentation is more discernible than 2, and code occupies less horizontal screen space than 8 spaces indentation. Preprocessor directives should be indented, as it makes a clear difference in ease of readability.

### Casing

| Item                                  | Style                                                          |
| ------------------------------------- | -------------------------------------------------------------- |
| Variables                             | `snake_case`                                                   |
| Functions and methods                 | `snake_case`                                                   |
| Namespaces                            | `snake_case`                                                   |
| `struct`, `enum`, and `union`'s in C  | `snake_case` (Add `_t` suffix for `typedef`'s: `snake_case_t`) |
| `class`, `enum`, and `union`'s in C++ | `PascalCase`                                                   |
| Constants, enum constants, macros     | `SCREAMING_SNAKE_CASE`                                         |

### Braces

#### Newline braces

Put opening brace on a new line with:
- `namespace`
- `extern`
- `class`
- Functions
- Methods

#### Same line braces

Put opening brace on the same line with:
- `struct`
- `enum`
- `union`
- Control statements
- Loops
- `try`, `catch`
- Lambdas

**Exception:** With multiline statements, prefer new-line braces instead of same-line braces for better readability.

For example:
```c++
if (xaaaaaaaaaaaaaaaaaaaaaaaaaa && yeeeeeeeeeeeeeeeeeeee
    && zeeeeeeeeeeeeeeeeeeeeee)
{
    // ...
}
```

#### Rationale

One rationale is to make a distinction between similar looking but different language constructs: to discern namespaces, extern statements, and classes from structs, enums, and unions; and to discern discern functions and methods from control statements, loops, try-catch blocks, and lambdas.

The other is that this style for braces is the intersection of most common conventions among C and C++ code.

### Classes and structs

#### Inheritance

Inheritance colon should have space before and after it. If the space is sufficient, put the inherited classes on the same line, otherwise put them on a new line.

```c++
class Platyrrhine : Primate
{};

class HomoSapien
    : HomoErectus
    , Neanderthal
{};
```

#### Make a distinction between classes and structs (only for C++)

In C++, you can use both `class` and `struct` keyword for classes. Make a clear distinction between `class` and `struct`: If the class or struct in question is data-only — it only consists of variables —, use `struct` keyword, put opening curly brace on the same line, and do not use member prefix (`m_`) for its variables. Otherwise, use `class` keyword, put opening curly brace on a new line, and use member prefix (`m_`) for member variables.

```c++
// Has a contructor. This is a class.
class Monkey
{
public:
    Monkey()
    {
        // ...
    }
};

// This is a struct.
// Notice that opening curly brace is not on a new line, and members are not prefixed with m_
struct Chimpanzee {
    std::string name;
    int age;
};
```

##### Rationale

In Rust and Go, structs only contain data, and functions are defined outside of struct. Conceptually, classes differ from structs: Classes have functions (called methods) inside them. It is more meaningful and precise to make a distinction between a data container (a struct) and a class, so we stick to that convention.

### Use single letter prefixes: Use `g_` for global variables, `s_` for static variables, and `m_` for class members

**Rationale:** Global variables, static variables, member variables, and local variables should not be confused with each other. For better safety, add prefix to global, static, and member variables.

```c++
int g_num_times_gibbered = 0;

class Ape
{
public:
    std::string m_name;
    uint8_t m_age;

    void gibber()
    {
        static int s_num_times_gibbered = 0;
        s_num_times_gibbered++;
        std::cout << m_name << " made a sound " << s_num_times_gibbered << " times" << std::endl;
        // Notice that without prefixes, s_num_times_gibbered and g_num_times_gibbered are the same.
        // If we had not added prefixes _s and _g to them, we would wrongly use the static variable
        // instead of the global variable in the below lines:
        g_num_times_gibbered++;
        std::cout << "All apes made a sound " << g_num_times_gibbered << " times" << std::endl;
    }
};

// Do not use a prefix within plain old data (POD) structs.
struct Monkey {
    char name[20];
    int age;
};
```

**Rationale specific to the `m_` prefix:** Let's consider other options: Using underscore (`_`) as a prefix is not feasible, as it is [reserved for implementation](https://www.iso.org/standard/79358.html) (compiler and standard library), and there are 3 options other than using `m_`: Using underscore (`_`) as suffix looks very bad and is difficult to discern at times; not using any prefix or suffix causes parameter shadowing, typing `this->name` is longer than `m_name`, and the member variable conflicts with other variable and function names with same name; using a letter other than "m" as prefix or suffix does not convey the meaning. Hence, `m_` prefix is the best option.

### Don not put space after the `template` keyword

```c++
// Wrong:
template <typename T>
// Right:
template<typename T>
```

**Rationale:**  This style is more Rust-like, and it makes it easier to distinguish templates from other language constructs.

