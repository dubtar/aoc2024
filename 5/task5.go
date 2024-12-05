package main

import (
	"bufio"
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func is_correct(nums []int, rules map[int][]int) bool {
	for i, n := range nums {
		for j := i + 1; j < len(nums); j++ {
			if slices.Contains(rules[nums[j]], n) {
				return false
			}
		}
	}
	return true
}

func main() {
	rules := make(map[int][]int)
	result1 := 0
	result2 := 0

	file, err := os.Open("input.txt")
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	rulesPart := true
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			rulesPart = false
			continue
		}
		if rulesPart {
			parts := strings.Split(line, "|")
			a, err := strconv.Atoi(parts[0])
			if err != nil {
				panic(err)
			}
			b, err := strconv.Atoi(parts[1])
			if err != nil {
				panic(err)
			}
			rules[a] = append(rules[a], b)
			continue
		}
		a_nums := strings.Split(line, ",")
		nums := make([]int, len(a_nums))
		for i, num := range a_nums {
			nums[i], err = strconv.Atoi(num)
			if err != nil {
				panic(err)
			}
		}
		is_valid := is_correct(nums, rules)
		if is_valid {
			result1 += nums[len(nums)/2]
		} else {
			for !is_valid {
				for i := 0; i < len(nums); i++ {
					for j := i + 1; j < len(nums); j++ {
						if slices.Contains(rules[nums[j]], nums[i]) {
							nums[j], nums[i] = nums[i], nums[j]
							break
						}
					}
				}
				is_valid = is_correct(nums, rules)
			}
			result2 += nums[len(nums)/2]
		}
	}
	fmt.Printf("Result 1: %d \n", result1)
	fmt.Printf("Result 2: %d \n", result2)
}
