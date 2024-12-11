package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"
	"sync/atomic"
)

func run(stone int64, runs int) int64 {
	for ; runs > 0; runs-- {
		if stone == 0 {
			stone = 1
			continue
		}
		s := strconv.FormatInt(stone, 10)
		length := len(s)
		if length%2 == 1 {
			stone *= 2024
		} else {
			a1, err := strconv.ParseInt(s[:length/2], 10, 64)
			if err != nil {
				panic(err)
			}
			a2, err := strconv.ParseInt(s[length/2:], 10, 64)
			if err != nil {
				panic(err)
			}
			return run(a1, runs-1) +
				run(a2, runs-1)
		}
	}
	return 1
}

func doFile(filename string, runs int) int64 {
	file, err := os.Open(filename)
	if err != nil {
		panic(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	wg := sync.WaitGroup{}
	scanner.Scan()
	line := scanner.Text()
	result := int64(0)
	for _, s := range strings.Split(line, " ") {
		if s == "" {
			continue
		}
		wg.Add(1)
		n, err := strconv.ParseInt(s, 10, 64)
		if err != nil {
			panic(err)
		}
		go func(n int64) {
			defer wg.Done()
			atomic.AddInt64(&result, run(n, runs))
		}(n)
	}
	wg.Wait()
	return result
}
func main() {

	fmt.Print("TEst: 55312==", doFile("test.txt", 25))
	fmt.Print("Result1=", doFile("input.txt", 25))
	fmt.Print("Result2=", doFile("input.txt", 75))

	// with Path(__file__).with_name('test.txt').open() as f:
	//     print('Test: 55312 == ', main(f, 25, verbose=False))

	// with Path(__file__).with_name('input.txt').open() as f:
	//
	//	# print('Result1:', main(f, 25))
	//	print('Result2:', main(f, 75))  # noqa: T201
}
