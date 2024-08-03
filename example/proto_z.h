#ifndef PROTO_Z_H
#define PROTO_Z_H

#include <cstdint>
#include <string>

// proto-z is an imaginary interstellar communication protocol.
namespace proto_z
{
    enum class Locations {
        AlphaCentauri,
        ProximaCentauri,
        Sirius,
        Betelgeuse,
        AndromedaGalaxy
    };

    struct Addr {
        Locations locations;
        uint64_t field1;
        uint64_t field2;
        uint64_t field3;
    };

    struct Header {
        Addr from;
        Addr to;
        std::string message;
    };

    class InterstellarLink
    {
    protected:
        static int s_send_count;

    public:
        virtual void send_message(const Addr &to, const std::string &message)
            = 0;
        virtual void recv_message(const Addr &from, const std::string &message)
            = 0;

        InterstellarLink() = default;

        InterstellarLink(const InterstellarLink &other) = default;
        InterstellarLink(InterstellarLink &&other) = default;

        InterstellarLink &operator=(const InterstellarLink &other) = default;
        InterstellarLink &operator=(InterstellarLink &&other) = default;

        virtual ~InterstellarLink() = default;
    };

    class Server : InterstellarLink
    {
        Addr m_addr;

    public:
        explicit Server(Addr addr) : m_addr(addr) {}

        void send_message(const Addr &to, const std::string &message) override;
        void recv_message(const Addr &to, const std::string &message) override;
    };

    class Client : InterstellarLink
    {
        Addr m_addr;

    public:
        explicit Client(Addr addr) : m_addr(addr) {}

        void send_message(const Addr &to, const std::string &message) override;
        void recv_message(const Addr &to, const std::string &message) override;
    };
}

#endif
