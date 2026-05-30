package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.AuthorDTO;
import com.example.pocapi.model.entity.Author;
import com.example.pocapi.repository.AuthorRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("AuthorService Unit Tests")
class AuthorServiceTest {
    
    @Mock
    private AuthorRepository authorRepository;
    
    @Mock
    private BookService bookService;
    
    @Mock
    private ReviewService reviewService;
    
    @InjectMocks
    private AuthorService authorService;
    
    private Author testAuthor;
    private AuthorDTO testAuthorDTO;
    
    @BeforeEach
    void setUp() {
        testAuthor = Author.builder()
                .id(1L)
                .firstName("Test")
                .lastName("Author")
                .email("test@example.com")
                .build();
        
        testAuthorDTO = AuthorDTO.builder()
                .firstName("Test")
                .lastName("Author")
                .email("test@example.com")
                .build();
    }
    
    @Test
    @DisplayName("should create author successfully")
    void testCreateAuthorSuccess() {
        // Arrange
        when(authorRepository.findByEmail(testAuthorDTO.getEmail())).thenReturn(Optional.empty());
        when(authorRepository.save(any(Author.class))).thenReturn(testAuthor);
        
        // Act
        AuthorDTO result = authorService.createAuthor(testAuthorDTO);
        
        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getFirstName()).isEqualTo("Test");
        assertThat(result.getLastName()).isEqualTo("Author");
        assertThat(result.getEmail()).isEqualTo("test@example.com");
        verify(authorRepository, times(1)).save(any(Author.class));
    }
    
    @Test
    @DisplayName("should throw validation exception when email is empty")
    void testCreateAuthorWithEmptyEmail() {
        // Arrange
        AuthorDTO invalidDTO = AuthorDTO.builder()
                .firstName("Test")
                .lastName("Author")
                .email("")
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> authorService.createAuthor(invalidDTO))
                .isInstanceOf(ValidationException.class)
                .hasMessage("Author email cannot be empty");
        
        verify(authorRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("should throw validation exception when email is invalid")
    void testCreateAuthorWithInvalidEmail() {
        // Arrange
        AuthorDTO invalidDTO = AuthorDTO.builder()
                .firstName("Test")
                .lastName("Author")
                .email("invalid-email")
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> authorService.createAuthor(invalidDTO))
                .isInstanceOf(ValidationException.class)
                .hasMessage("Author email must be valid");
        
        verify(authorRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("should throw validation exception when duplicate email")
    void testCreateAuthorWithDuplicateEmail() {
        // Arrange
        when(authorRepository.findByEmail(testAuthorDTO.getEmail())).thenReturn(Optional.of(testAuthor));
        
        // Act & Assert
        assertThatThrownBy(() -> authorService.createAuthor(testAuthorDTO))
                .isInstanceOf(ValidationException.class)
                .hasMessage("Author with email test@example.com already exists");
        
        verify(authorRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("should get author by id successfully")
    void testGetAuthorByIdSuccess() {
        // Arrange
        when(authorRepository.findById(1L)).thenReturn(Optional.of(testAuthor));
        
        // Act
        AuthorDTO result = authorService.getAuthorById(1L);
        
        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getFirstName()).isEqualTo("Test");
        assertThat(result.getLastName()).isEqualTo("Author");
        verify(authorRepository, times(1)).findById(1L);
    }
    
    @Test
    @DisplayName("should throw exception when author not found")
    void testGetAuthorByIdNotFound() {
        // Arrange
        when(authorRepository.findById(999L)).thenReturn(Optional.empty());
        
        // Act & Assert
        assertThatThrownBy(() -> authorService.getAuthorById(999L))
                .isInstanceOf(ResourceNotFoundException.class)
                .hasMessage("Author not found with id: 999");
        
        verify(authorRepository, times(1)).findById(999L);
    }
}
