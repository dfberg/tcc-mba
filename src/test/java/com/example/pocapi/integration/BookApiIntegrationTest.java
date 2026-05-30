package com.example.pocapi.integration;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.example.pocapi.model.dto.AuthorDTO;
import com.example.pocapi.model.dto.BookDTO;
import com.example.pocapi.repository.AuthorRepository;
import com.example.pocapi.repository.BookRepository;
import com.example.pocapi.repository.ReviewRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import org.approvaltests.Approvals;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@DisplayName("Book API Integration Tests with Snapshots")
class BookApiIntegrationTest {
    
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Autowired
    private AuthorRepository authorRepository;
    
    @Autowired
    private BookRepository bookRepository;
    
    @Autowired
    private ReviewRepository reviewRepository;
    
    private Long authorId;
    
    @BeforeEach
    void setUp() throws Exception {
        // Clear data before each test
        reviewRepository.deleteAll();
        bookRepository.deleteAll();
        authorRepository.deleteAll();
        
        // Create sample author
        AuthorDTO authorDTO = AuthorDTO.builder()
                .firstName("Arthur")
                .lastName("Conan Doyle")
                .email("doyle@example.com")
                .build();
        
        MvcResult result = mockMvc.perform(post("/authors")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(authorDTO)))
                .andExpect(status().isCreated())
                .andReturn();
        
        String authorJson = result.getResponse().getContentAsString();
        AuthorDTO createdAuthor = objectMapper.readValue(authorJson, AuthorDTO.class);
        authorId = createdAuthor.getId();
    }
    
    @Test
    @DisplayName("should create book - snapshot test")
    void testCreateBook_Snapshot() throws Exception {
        // Arrange
        BookDTO bookDTO = BookDTO.builder()
                .title("The Hound of the Baskervilles")
                .isbn("978-0-14-043926-8")
                .authorId(authorId)
                .build();
        
        // Act
        MvcResult result = mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(bookDTO)))
                .andExpect(status().isCreated())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
    
    @Test
    @DisplayName("should get books by author - snapshot test")
    void testGetBooksByAuthor_Snapshot() throws Exception {
        // Arrange
        BookDTO bookDTO1 = BookDTO.builder()
                .title("Sherlock Holmes: A Study in Scarlet")
                .isbn("978-0-14-043924-4")
                .authorId(authorId)
                .build();
        
        BookDTO bookDTO2 = BookDTO.builder()
                .title("The Sign of the Four")
                .isbn("978-0-14-043925-1")
                .authorId(authorId)
                .build();
        
        mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(bookDTO1)))
                .andExpect(status().isCreated());
        
        mockMvc.perform(post("/books")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(bookDTO2)))
                .andExpect(status().isCreated());
        
        // Act
        MvcResult result = mockMvc.perform(get("/books/by-author/" + authorId)
                .contentType(MediaType.APPLICATION_JSON))
                .andExpect(status().isOk())
                .andReturn();
        
        String responseBody = result.getResponse().getContentAsString();
        
        // Assert - Snapshot verification
        Approvals.verify(responseBody);
    }
}
