package com.example.pocapi.model.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class ReviewDTO {
    
    private Long id;
    private Integer rating;
    private String content;
    private Long bookId;
    private String bookTitle;
    
    // Constructor for creating new review (without id)
    public ReviewDTO(Integer rating, String content, Long bookId) {
        this.rating = rating;
        this.content = content;
        this.bookId = bookId;
    }
}
