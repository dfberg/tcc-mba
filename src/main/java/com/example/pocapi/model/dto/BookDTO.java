package com.example.pocapi.model.dto;

import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.util.List;

@Data
@NoArgsConstructor
@AllArgsConstructor
@Builder
@JsonInclude(JsonInclude.Include.NON_NULL)
public class BookDTO {
    
    private Long id;
    private String title;
    private String isbn;
    private Long authorId;
    private String authorName;
    private List<ReviewDTO> reviews;
    
    // Constructor for creating new book (without id and reviews)
    public BookDTO(String title, String isbn, Long authorId) {
        this.title = title;
        this.isbn = isbn;
        this.authorId = authorId;
    }
}
