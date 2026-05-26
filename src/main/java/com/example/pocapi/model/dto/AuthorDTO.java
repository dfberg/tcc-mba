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
public class AuthorDTO {
    
    private Long id;
    private String name;
    private String email;
    private List<BookDTO> books;
    
    // Constructor for creating new author (without id and books)
    public AuthorDTO(String name, String email) {
        this.name = name;
        this.email = email;
    }
}
