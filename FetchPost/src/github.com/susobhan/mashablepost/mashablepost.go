package main
import (
	"github.com/sadlil/mashable"
	"fmt"
	"encoding/csv"
	"os"
	"io"
)

func main() {

	f, err := os.Open("OnlineNewsPopularity.csv")
	if err != nil {
		panic("Cannot open file OnlineNewsPopularity.csv")
	}
	defer f.Close()

	csvdata := csv.NewReader(f)

	i := 0
	for {
		row, err := csvdata.Read()
		if err != nil {
			if err == io.EOF {
				err = nil
				break
			} else {
				panic("Cannot read data")
			}
		}
		if i == 0 {
			i = i + 1
			continue
		}

		c, err := mashable.New()
		if err != nil {
			panic("client creation failed")
		}
		// fmt.Printf(row[0] + "\n")
		post, err := c.Posts().GetFromUrl(row[0])
		if err != nil {
			panic("Couldn't fetch url: " + row[0])
		}
		postcontent := post.Full
		fmt.Printf(postcontent.Full + "\n\n")
		i = i + 1
	}


	
}