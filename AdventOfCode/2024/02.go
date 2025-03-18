package main

import (
  "bufio"
  "fmt"
  "os"
  "strconv"
  "strings"
)

// Read the input data from "input.txt" file. Parse each line into a slice of
// integers, creating a 2D slice of integers where each inner slice represents
// a line in the reports file. If an error occurs during file reading or
// conversion, the function panics.
func readPuzzleInput() [][]int {
  file, err := os.Open("../input.txt")
  if err != nil {
    panic(err)  // Terminate the program if the file cannot be opened
  }
  defer file.Close()  // Ensure the file is closed when the function exits

  var reports [][]int  // Slice to hold the parsed data

  // Read the file line-by-line
  scanner := bufio.NewScanner(file)
  for scanner.Scan() {
    line := scanner.Text()  // Read single line of text
    fields := strings.Fields(line)  // Split line into fields by whitespace
    var report []int

    // Convert each field to an integer
    for _, field := range fields {
      value, err := strconv.Atoi(field)
      if err != nil {
        panic(err)  // Terminate if a field cannot be converted to an integer
      }
      report = append(report, value)
    }
    reports = append(reports, report)  // Add the parsed line to the reports
  }

  if err := scanner.Err(); err != nil {
    panic(err)  // Handle any errors that occurred during scanning
  }

  return reports
}

// Check if report is "safe" based on specific criteria:
//   - A report is considered "increasing" if differences between consecutive
//     numbers are between 1 & 3 (inclusive)
//   - A report is considered "decreasing" if differences between consecutive
//     numbers are between -1 & -3 (inclusive)
// Return "true" if the report is either increasing or decreasing
func isSafe(report[]int) bool {
  increasing := true
  decreasing := true

  for i := 1; i < len(report); i++ {
    diff := report[i] - report[i-1]

    if diff < 1 || diff > 3 {
      increasing = false
    }
    if diff < -3 || diff > -1 {
      decreasing = false
    }
  }

  return increasing || decreasing
}

// Check if a report can become "safe" by removing one element. For each
// element in the report, the function creates a new slice excluding that
// element and checks if the new slice is "safe" using "isSafe()". Returns
// "true" if removing a single element results in a safe report.
func canBeSafe(report[]int) bool {
  for i := 0; i < len(report); i++ {
    // Create a new slice excluding the element at index i
    newReport := append([]int{}, report[:i]...)    // Copy elements before i
    newReport = append(newReport, report[i+1:]...) // Append elements after i

    if isSafe(newReport) {
      return true
    }
  }
  return false
}

// Count how many reports in the given 2D slice are "safe". Uses the
// "isSafe()" function to determine if a report is safe. Returns the number of
// safe reports.
func partOne(reports[][]int) int {
  num_safe := 0
  for _, report := range reports {
    if isSafe(report) {
      num_safe += 1
    }
  }
  return num_safe
}

// Count how many reports in the given 2D slice are "safe" and can be made
// "safe" by removing a single element. It uses the "canBeSafe()" function
// for these checks.
func partTwo(reports[][]int) int {
  num_safe := 0
  for _, report := range reports {
    if canBeSafe(report) {
      num_safe += 1
    }
  }
  return num_safe
}

// Orchestrate the program flow by calling the inputer reading function and
// solving Part 1 and Part 2 of the puzzle.
func main() {
  reports := readPuzzleInput()
  fmt.Println("Part 1:", partOne(reports))  // 341
  fmt.Println("Part 2:", partTwo(reports))  // 404
}
