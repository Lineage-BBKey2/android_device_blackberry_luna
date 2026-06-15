#include <android/native_window.h>
#include <dlfcn.h>
#include <fcntl.h>
#include <stdarg.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/socket.h>

extern "C" {
    // This is the function a proprietary camera blob is looking for
    ANativeWindow* ANativeWindow_fromSurface(void* env, void* surface) {
        // Use dlsym to get the real function from libnativewindow.so
        static auto real_func = (ANativeWindow* (*)(void*, void*))dlsym(dlopen("libnativewindow.so", RTLD_NOW), "ANativeWindow_fromSurface");
        if (real_func) {
            return real_func(env, surface);
        }
        return nullptr;
    }

// --- Helper to resolve symbols from libc ---
    static void* get_libc_symbol(const char* name) {
        static void* libc = dlopen("libc.so", RTLD_NOW);
        return dlsym(libc, name);
    }

    // --- The __wrap_ symbols ---
    int __wrap_open(const char *pathname, int flags, mode_t mode) {
        typedef int (*open_t)(const char *, int, mode_t);
        static auto real_open = (open_t)get_libc_symbol("open");
        return real_open(pathname, flags, mode);
    }

    int __wrap_close(int fd) {
        typedef int (*close_t)(int);
        static auto real_close = (close_t)get_libc_symbol("close");
        return real_close(fd);
    }

    void* __wrap_malloc(size_t size) {
        typedef void* (*malloc_t)(size_t);
        static auto real_malloc = (malloc_t)get_libc_symbol("malloc");
        return real_malloc(size);
    }

    void __wrap_free(void* ptr) {
        typedef void (*free_t)(void*);
        static auto real_free = (free_t)get_libc_symbol("free");
        real_free(ptr);
    }

    int __wrap_pipe(int pipefd[2]) {
        typedef int (*pipe_t)(int*);
        static auto real_pipe = (pipe_t)get_libc_symbol("pipe");
        return real_pipe(pipefd);
    }

    int __wrap_socket(int domain, int type, int protocol) {
        typedef int (*socket_t)(int, int, int);
        static auto real_socket = (socket_t)get_libc_symbol("socket");
        return real_socket(domain, type, protocol);
    }
}


