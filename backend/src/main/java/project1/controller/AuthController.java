package project1.controller;
import project1.dto.LoginRequest;
import jakarta.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import project1.dto.AuthResponse;
import project1.dto.RegisterRequest;
import project1.entity.User;
import project1.service.AuthService;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    public ResponseEntity<AuthResponse> register(
            @Valid @RequestBody RegisterRequest request) {

        try {

            User user = authService.registerUser(
                    request.getUsername(),
                    request.getEmail(),
                    request.getPassword()
            );

            AuthResponse response = new AuthResponse(
                    true,
                    "User registered successfully",
                    user.getId(),
                    user.getUsername()
            );

            return ResponseEntity
                    .status(HttpStatus.CREATED)
                    .body(response);

        } catch (RuntimeException error) {

            AuthResponse response = new AuthResponse(
                    false,
                    error.getMessage(),
                    null,
                    null
            );

            return ResponseEntity
                    .badRequest()
                    .body(response);
        }
    }
    @PostMapping("/login")
    public ResponseEntity<AuthResponse> login(
            @Valid @RequestBody LoginRequest request) {

        try {

            User user = authService.loginUser(
                    request.getUsername(),
                    request.getPassword()
            );

            AuthResponse response = new AuthResponse(
                    true,
                    "Login successful",
                    user.getId(),
                    user.getUsername()
            );

            return ResponseEntity.ok(response);

        } catch (RuntimeException error) {

            AuthResponse response = new AuthResponse(
                    false,
                    error.getMessage(),
                    null,
                    null
            );

            return ResponseEntity
                    .status(HttpStatus.UNAUTHORIZED)
                    .body(response);
        }
    }
}