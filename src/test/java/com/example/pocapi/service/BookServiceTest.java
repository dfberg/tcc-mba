package com.example.pocapi.service;

import com.example.pocapi.exception.ResourceNotFoundException;
import com.example.pocapi.exception.ValidationException;
import com.example.pocapi.model.dto.BookDTO;
import com.example.pocapi.model.entity.Author;
import com.example.pocapi.model.entity.Book;
import com.example.pocapi.repository.AuthorRepository;
import com.example.pocapi.repository.BookRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Optional;

import static org.assertj.core.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.*;

@ExtendWith(MockitoExtension.class)
@DisplayName("BookService Unit Tests")
class BookServiceTest {
    
    @Mock
    private BookRepository bookRepository;
    
    @Mock
    private AuthorRepository authorRepository;
    
    @InjectMocks
    private BookService bookService;
    
    private Book testBook;
    private Author testAuthor;
    private BookDTO testBookDTO;
    
    @BeforeEach
    void setUp() {
        testAuthor = Author.builder()
                .id(1L)
                .name("Test Author")
                .email("test@example.com")
                .build();
        
        testBook = Book.builder()
                .id(1L)
                .title("Test Book")
                .isbn("123456789")
                .author(testAuthor)
                .build();
        
        testBookDTO = BookDTO.builder()
                .title("Test Book")
                .isbn("123456789")
                .authorId(1L)
                .build();
    }
    
    @Test
    @DisplayName("should create book successfully")
    void testCreateBookSuccess() {
        // Arrange
        when(authorRepository.findById(1L)).thenReturn(Optional.of(testAuthor));
        when(bookRepository.findByIsbn("123456789")).thenReturn(Optional.empty());
        when(bookRepository.save(any(Book.class))).thenReturn(testBook);
        
        // Act
        BookDTO result = bookService.createBook(testBookDTO);
        
        // Assert
        assertThat(result).isNotNull();
        assertThat(result.getTitle()).isEqualTo("Test Book");
        assertThat(result.getIsbn()).isEqualTo("123456789");
        verify(bookRepository, times(1)).save(any(Book.class));
    }
    
    @Test
    @DisplayName("should throw validation exception when title is empty")
    void testCreateBookWithEmptyTitle() {
        // Arrange
        BookDTO invalidDTO = BookDTO.builder()
                .title("")
                .isbn("123456789")
                .authorId(1L)
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> bookService.createBook(invalidDTO))
                .isInstanceOf(ValidationException.class)
                .hasMessage("Book title cannot be empty");
        
        verify(bookRepository, never()).save(any());
    }
    
    @Test
    @DisplayName("should throw exception when author not found")
    void testCreateBookWithInvalidAuthor() {
        // Arrange
        when(authorRepository.findById(999L)).thenReturn(Optional.empty());
        
        BookDTO invalidDTO = BookDTO.builder()
                .title("Test Book")
                .isbn("123456789")
                .authorId(999L)
                .build();
        
        // Act & Assert
        assertThatThrownBy(() -> bookService.createBook(invalidDTO))
                .isInstanceOf(ResourceNotFoundException.class);
        
        verify(bookRepository, never()).save(any());
    }
}
